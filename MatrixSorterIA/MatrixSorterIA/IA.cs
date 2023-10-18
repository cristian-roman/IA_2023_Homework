using System.Diagnostics;
using MatrixSorterIA.Models;

namespace MatrixSorterIA
{
    // ReSharper disable once InconsistentNaming
    public static class IA
    {
        private const int MaxDepth = 10000;
        private enum Direction
        {
            Up,
            Down,
            Left,
            Right
        }
        
        private static StateModel? _initialState;
        public static void Start(IEnumerable<int> input)
        {
            _initialState = new StateModel(TurnInputToMatrix(input));
            Iddfs(_initialState!);
        }

        private static void Iddfs(StateModel initialState)
        {
            foreach (var depth in Enumerable.Range(0, MaxDepth))
            {
                var visitedStates = new HashSet<StateModel>();
                
                var solution = DepthLimitedDfs(initialState, depth, visitedStates);
                
                if (solution == null) continue;
                
                
                Console.WriteLine();
                Console.WriteLine("Found solution:");
                Console.WriteLine(solution);
                return;
            }
            
            Console.WriteLine("No solution found");
        }

        private static StateModel? DepthLimitedDfs(StateModel currentState, int depth, ISet<StateModel> visited)
        {
            if (currentState.IsFinalState())
                return currentState;

            if (depth <= 0)
                return null;
            
            visited.Add(currentState);
            
            foreach (var direction in Enum.GetValues(typeof(Direction)))
            {
                var nextState = ToNextState(currentState, (Direction) direction);
                if (nextState == null || visited.Contains(nextState))
                    continue;
                
                var solution = DepthLimitedDfs(nextState, depth - 1, visited);
                if (solution != null)
                    return solution;
            }

            return null;
        }
    
        // step 2 - metoda de parsare a inputului ca stare intiala
        private static int[,] TurnInputToMatrix(IEnumerable<int> input)
        {
            var initialState = new int[3, 3];
            
            var row = 0; 
            var column = 0;
        
            foreach (var element in input)
            {
                initialState[row, column] = element;
                
                column++;
                if (column != 3) continue;
                row++;
                column = 0;
            }

            return initialState;
        }

        
        // step - 3 metoda de trecere la un nou state si daca acesta este valid
        private static StateModel? ToNextState(StateModel currentState, Direction emptyCellMovement)
        { 
            if(IsNewStateOutBounded(currentState, emptyCellMovement)) 
                return null;
            
            if(IsNextStateGoingBackward(currentState, emptyCellMovement))
                return null;

            var newStateMatrix = currentState.Matrix;
            
            var nextZeroedLocationExpected = GetNextZeroedLocationExpected(currentState.CurrentZeroedCellLocation!, emptyCellMovement);
            
            //swap the values
            
            (newStateMatrix[currentState.CurrentZeroedCellLocation!.Y, currentState.CurrentZeroedCellLocation!.X], newStateMatrix[nextZeroedLocationExpected.Y, nextZeroedLocationExpected.X]) = 
                (newStateMatrix[nextZeroedLocationExpected.Y, nextZeroedLocationExpected.X], newStateMatrix[currentState.CurrentZeroedCellLocation!.Y, currentState.CurrentZeroedCellLocation!.X]);

            return new StateModel(currentState.Matrix, 
                nextZeroedLocationExpected, 
                currentState.CurrentZeroedCellLocation!);
        }

        private static bool IsNewStateOutBounded(StateModel currentState, Direction emptyCellMovement)
        {
            switch (emptyCellMovement)
            {
                case Direction.Up:
                    if(currentState.CurrentZeroedCellLocation!.Y == 0)
                        return true;
                    break;
                case Direction.Down:
                    if(currentState.CurrentZeroedCellLocation!.Y == 2)
                        return true;
                    break;
                case Direction.Left:
                    if(currentState.CurrentZeroedCellLocation!.X == 0)
                        return true;
                    break;
                case Direction.Right:
                    if(currentState.CurrentZeroedCellLocation!.X == 2)
                        return true;
                    break;
                default:
                    throw new Exception("Invalid direction");
            }
            
            return false;
        }

        private static bool IsNextStateGoingBackward(StateModel currentState, Direction emptyCellMovement)
        {
            var nextZeroedCellLocation = GetNextZeroedLocationExpected(currentState.CurrentZeroedCellLocation!, emptyCellMovement);
            
            return nextZeroedCellLocation.Equals(currentState.PreviousZeroedCellLocation);
        }

        private static CellLocation GetNextZeroedLocationExpected(CellLocation currentZeroedCellLocation, Direction emptyCellMovement)
        {
            return emptyCellMovement switch
            {
                Direction.Up => new CellLocation(currentZeroedCellLocation.X, currentZeroedCellLocation.Y - 1),
                Direction.Down => new CellLocation(currentZeroedCellLocation.X, currentZeroedCellLocation.Y + 1),
                Direction.Left => new CellLocation(currentZeroedCellLocation.X - 1, currentZeroedCellLocation.Y),
                Direction.Right => new CellLocation(currentZeroedCellLocation.X + 1, currentZeroedCellLocation.Y),
                _ => throw new Exception("Invalid direction")
            };
        }
    }
}