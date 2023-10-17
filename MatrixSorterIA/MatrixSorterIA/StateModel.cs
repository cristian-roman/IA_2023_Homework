namespace MatrixSorterIA;

public class StateModel
{
    //step 1 - create the state model
    public class Cell
    {
        public int X { get; set; }
        public int Y { get; set; }
        
        public Cell(int x, int y)
        {
            X = x;
            Y = y;
        }
    }
    public int[,] Matrix { get; set; }
    public Cell? ZeroedCell { get; set; }
    
    public StateModel(int[,] input)
    {
        Matrix = input;
        ZeroedCell = GetZeroedCell();
    }

    private Cell? GetZeroedCell()
    {
        for (var i = 0; i < 3; i++)
        {
            for (var j = 0; j < 3; j++)
            {
                if (Matrix[i,j] == 0)
                    return new Cell(i, j);
            }
        }

        return null;
    }
}