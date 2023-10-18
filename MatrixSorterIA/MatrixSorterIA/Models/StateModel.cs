namespace MatrixSorterIA.Models;

public class StateModel
{
    //step 1 - create the state model

    public int[,] Matrix { get; }

    public CellLocation? PreviousZeroedCellLocation { get;}

    private CellLocation? _currentZeroedCellLocation;
    public CellLocation? CurrentZeroedCellLocation
    {
        get { return _currentZeroedCellLocation ??= SearchZeroedCell(); }
    }
    
    public StateModel(int[,] input)
    {
        Matrix = input;
        _currentZeroedCellLocation = null;
        PreviousZeroedCellLocation = null;
    }

    public StateModel(int[,] state, CellLocation currentZeroedCellLocation, CellLocation previousZeroedCellLocation)
    {
        Matrix = state;
        _currentZeroedCellLocation = currentZeroedCellLocation;
        PreviousZeroedCellLocation = previousZeroedCellLocation;
    }

    private CellLocation? SearchZeroedCell()
    {
        for (var i = 0; i < 3; i++)
        {
            for (var j = 0; j < 3; j++)
            {
                if (Matrix[i,j] == 0)
                    return new CellLocation(i, j);
            }
        }

        return null;
    }
    
    // step 2 -- metoda de verificare ca stare finala
    public static bool IsFinalState(int[,] state)
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
}