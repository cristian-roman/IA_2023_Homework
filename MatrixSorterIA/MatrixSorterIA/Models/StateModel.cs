using System.Security.Cryptography;
using System.Text;

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
                    return new CellLocation(j, i);
            }
        }

        return null;
    }
    
    // step 2 -- metoda de verificare ca stare finala
    public bool IsFinalState()
    {
        var toCompare = 1;
            
        for(var i = 0; i < 3; i++)
        for (var j = 0; j < 3; j++)
        {
            if(Matrix[i,j] == 0)
                continue;
                
            if(Matrix[i,j] != toCompare)
                return false;
                
            toCompare++;
        }

        return true;
    }

    public override bool Equals(object? obj)
    {
        if (obj == null)
        {
            return false;
        }

        if (obj.GetType() != typeof(StateModel))
        {
            return false;
        }

        var otherState = (StateModel)obj;
        
        for(var i = 0; i < 3; i++)
            for(var j = 0; j < 3; j++)
                if(Matrix[i,j] != otherState.Matrix[i,j])
                    return false;

        return true;
    }

    public override string ToString()
    {
        var sb = new StringBuilder();
        for(var i = 0; i < 3; i++)
        {
            for(var j = 0; j < 3; j++)
                sb.Append($"{Matrix[i,j]} ");
            sb.AppendLine();
        }
        
        return sb.ToString();
    }
    
    public override int GetHashCode()
    {
        var stringBuilder = new StringBuilder();

        // Concatenate all elements of the matrix into a string
        for (var i = 0; i < Matrix.GetLength(0); i++)
        {
            for (var j = 0; j < Matrix.GetLength(1); j++)
            {
                stringBuilder.Append(Matrix[i, j]);
            }
        }

        // Compute SHA-256 hash
        var hashBytes = SHA256.HashData(Encoding.UTF8.GetBytes(stringBuilder.ToString()));
        var hashBuilder = new StringBuilder();
        foreach (var b in hashBytes)
        {
            hashBuilder.Append(b.ToString("x2"));
        }
        return hashBuilder.ToString().GetHashCode();
    }
}