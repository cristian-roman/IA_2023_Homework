using System.Diagnostics;
using MatrixSorterIA.Models;

namespace MatrixSorterIA
{
    // ReSharper disable once InconsistentNaming
    public static class IA
    {
        private const int MaxDepth = 10000;
        
        private static IList<StateModel>? _finalStateModels;
        private delegate int HeuristicFunction(StateModel state, StateModel finalState);

        private static int _numberOfMoves;

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
            _finalStateModels = new List<StateModel>();
            for(var i = 0; i < 3; i++)
            {
                for(var j = 0; j < 3; j++)
                {
                    var zeroCellLocation = new CellLocation(j, i);
                    _finalStateModels.Add(StateModel.GetFinalStateWithZeroOnPosition(zeroCellLocation));
                }
            }
            _numberOfMoves = 0;

            Console.WriteLine("Iddfs summary:");
            var watch = Stopwatch.StartNew();
            Iddfs(_initialState!);
            watch.Stop();
            Console.WriteLine("Time elapsed: " + watch.ElapsedMilliseconds + "ms");
            
            Console.WriteLine();
            Console.WriteLine("BfsGreedy with EuclideanDistance heuristic summary:");
            watch = Stopwatch.StartNew();
            BfsGreedy(_initialState, EuclideanDistanceHeuristic);
            watch.Stop();
            Console.WriteLine("Time elapsed: " + watch.ElapsedMilliseconds + "ms");
            
            Console.WriteLine();
            Console.WriteLine("BfsGreedy with ManhattanDistance heuristic summary:");
            watch = Stopwatch.StartNew();
            BfsGreedy(_initialState, ManhattanDistanceHeuristic);
            watch.Stop();
            Console.WriteLine("Time elapsed: " + watch.ElapsedMilliseconds + "ms");
            
            Console.WriteLine();
            Console.WriteLine("BfsGreedy with HammingDistance heuristic summary:");
            watch = Stopwatch.StartNew();
            BfsGreedy(_initialState, HammingDistanceHeuristic);
            watch.Stop();
            Console.WriteLine("Time elapsed: " + watch.ElapsedMilliseconds + "ms");
            
            Console.WriteLine();
            Console.WriteLine("AStarBfs summary:");
            watch = Stopwatch.StartNew();
            AStarBfs(_initialState, EuclideanDistanceHeuristic);
            watch.Stop();
            Console.WriteLine("Time elapsed: " + watch.ElapsedMilliseconds + "ms");
        }

        private static void Iddfs(StateModel initialState)
        {
            foreach (var depth in Enumerable.Range(0, MaxDepth))
            {
                var visitedStates = new HashSet<StateModel>();
                
                var solution = DepthLimitedDfs(initialState, depth, visitedStates);
                
                if (solution == null) continue;
                
                
                Console.WriteLine("Found solution:");
                Console.Write(solution);
                Console.WriteLine("Number of moves: " + depth);
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

            var newStateMatrix = new int[3,3];
            Array.Copy(currentState.Matrix, newStateMatrix, 9);
            
            var nextZeroedLocationExpected = GetNextZeroedLocationExpected(currentState.CurrentZeroedCellLocation!, emptyCellMovement);
            
            newStateMatrix[currentState.CurrentZeroedCellLocation!.Y, currentState.CurrentZeroedCellLocation!.X] = 
                newStateMatrix[nextZeroedLocationExpected.Y, nextZeroedLocationExpected.X];
            
            newStateMatrix[nextZeroedLocationExpected.Y, nextZeroedLocationExpected.X] = 0;

            return new StateModel(newStateMatrix, 
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
        private static int CalculateHeuristicScore(StateModel state, HeuristicFunction heuristicFunction)
        {
            var score = heuristicFunction(state, _finalStateModels![0]);
            for(var i = 1; i < _finalStateModels.Count; i++)
            {
                score = Math.Min(score, heuristicFunction(state, _finalStateModels[i]));
            }
            return score;
        }
        
        private static int ManhattanDistanceHeuristic(StateModel state, StateModel finalState)
        {
            var sum = 0;
            
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                var currentElement = state.Matrix[i, j];
                if (currentElement == 0)
                    continue;

                var expectedLocation = SearchCellInFinalStateModel(currentElement, finalState);
                sum += Math.Abs(expectedLocation.X - j) + Math.Abs(expectedLocation.Y - i);
            }

            return sum;
        }
        
        private static CellLocation SearchCellInFinalStateModel(int element, StateModel finalState)
        {
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
                if (finalState.Matrix[i, j] == element)
                    return new CellLocation(j, i);

            throw new Exception("Element not found");
        }

        private static int HammingDistanceHeuristic(StateModel state, StateModel finalState)
        {
            var ans = 0;
            for(var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                if (finalState.Matrix[i, j] != state.Matrix[i, j])
                {
                    ans++;
                }
            }

            return ans;
        }
        
        private static int EuclideanDistanceHeuristic(StateModel state, StateModel finalState)
        {
            var sum = 0d;
            
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                var currentElement = state.Matrix[i, j];
                if (currentElement == 0)
                    continue;

                var expectedLocation = SearchCellInFinalStateModel(currentElement, finalState);
                sum += Math.Sqrt(Math.Pow(expectedLocation.X - j, 2) + Math.Pow(expectedLocation.Y - i, 2));
            }

            return (int)sum;
        }

        private static void BfsGreedy(StateModel initialState, HeuristicFunction heuristicFunction)
        {
            var visited = new Dictionary<StateModel, int>();
            var queue = new PriorityQueue<StateModel, int>();
            
            queue.Enqueue(initialState, 0);
                
            while (queue.Count > 0)
            {
                var currentState = queue.Dequeue();
                if(visited.ContainsKey(currentState))
                    continue;

                var parentState = currentState.GetPreviousState();

                if(parentState.Equals(currentState))
                    visited.Add(currentState, 0);
                else
                    visited.Add(currentState, visited[parentState] + 1);

                if (currentState.IsFinalState())
                {
                    Console.WriteLine("Found solution:");
                    Console.Write(currentState);
                    _numberOfMoves = visited[currentState];
                    Console.WriteLine("Number of moves: " + _numberOfMoves);
                    return;
                }

                foreach (var direction in Enum.GetValues(typeof(Direction)))
                {
                    var nextState = ToNextState(currentState, (Direction) direction);
                    if (nextState == null || visited.ContainsKey(nextState))
                        continue;
                        
                    var nextStateDistance = CalculateHeuristicScore(nextState, heuristicFunction);
                    
                    queue.Enqueue(nextState, nextStateDistance);
                }
            }
            
            Console.WriteLine("No solution found");
        }

        private static void AStarBfs(StateModel initialState, HeuristicFunction heuristic)
        {
            var visited = new Dictionary<StateModel, int>();
            var lengths = new Dictionary<StateModel, int>();
            var queue = new PriorityQueue<StateModel, int>();
            
            queue.Enqueue(initialState, 0);
            lengths.Add(initialState, 0);
                
            while (queue.Count > 0)
            {
                var currentState = queue.Dequeue();
                if(visited.ContainsKey(currentState))
                    continue;
                
                var parentState = currentState.GetPreviousState();
                if(parentState.Equals(currentState))
                    visited.Add(currentState, 0);
                else
                    visited.Add(currentState, visited[parentState] + 1);

                if (currentState.IsFinalState())
                {
                    Console.WriteLine("Found solution:");
                    Console.Write(currentState);
                    _numberOfMoves = visited[currentState];
                    Console.WriteLine("Number of moves: " + _numberOfMoves);
                    return;
                }

                foreach (var direction in Enum.GetValues(typeof(Direction)))
                {
                    var nextState = ToNextState(currentState, (Direction) direction);
                    if (nextState == null || visited.ContainsKey(nextState))
                        continue;
                        
                    var nextStateDistance = CalculateHeuristicScore(nextState, heuristic);
                    
                    queue.Enqueue(nextState, -(nextStateDistance + lengths[currentState]));
                    
                    if(lengths.TryGetValue(nextState, out var traveledDistance))
                        lengths[nextState] = Math.Min(nextStateDistance + traveledDistance, lengths[nextState]);
                    else
                        lengths.Add(nextState, nextStateDistance + lengths[currentState]);
                }
            }
            
            Console.WriteLine("No solution found");
        }

    }
}