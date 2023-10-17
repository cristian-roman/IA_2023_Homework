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
            _initialState = new StateModel(GetInitialState(input));
        }
    
        // step 2 - metoda de parsare a inputului ca stare intiala si metoda de verificare ca stare finala
        private static int[,] GetInitialState(IEnumerable<int> input)
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

        private static bool IsFinalState(int[,] state)
        {
            var toCompare = 1;
            
            for(var i = 0; i < 3; i++)
                for (var j = 0; j < 3; j++)
            {
                if(state[i,j] == 0)
                    continue;
                
                if(state[i,j] != toCompare)
                    return false;
                
                toCompare++;
            }

            return true;
        }

        // private static int[,] ToNextState(int[,] currentState, Direction emptyCellMovement)
        // {
        //     
        // }
    }
}