using System.Diagnostics;
using MatrixSorterIA.Models;

namespace MatrixSorterIA
{
    // ReSharper disable once InconsistentNaming
    public static class IA
    {
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

        private static StateModel? ToNextState(StateModel currentState, Direction emptyCellMovement)
        { 
            if(IsNewStateOutBounded(currentState, emptyCellMovement)) 
                return null;
            
            if(IsNextStateGoingBackward(currentState, emptyCellMovement))
                return null;
            
            return new StateModel(currentState.Matrix, 
                GetNextZeroedLocationExpected(currentState.CurrentZeroedCellLocation!, emptyCellMovement), 
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