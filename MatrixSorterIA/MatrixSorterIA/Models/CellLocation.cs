namespace MatrixSorterIA.Models;

public class CellLocation
{
    //step 1 - create the state model
    public int X { get; set; }
    public int Y { get; set; }
        
    public CellLocation(int x, int y)
    {
        X = x;
        Y = y;
    }

    public override bool Equals(object? obj)
    {
        if (obj == null)
            return false;
        if (obj.GetType() != typeof(CellLocation))
            return false;
        var other = (CellLocation) obj;
        return other.X == X && other.Y == Y;
    }
}