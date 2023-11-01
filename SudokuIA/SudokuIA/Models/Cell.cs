namespace SudokuIA.Models;

public class Cell
{
    public short Row { get; }
    public short Column { get; }
    public short Value { get; set; }
    public bool IsFixed { get; set; }
    public bool IsGrayedCell { get; }
    
    public HashSet<Cell> Removers { get; } 
    public List<short> Domain { get; }
    
    public Cell(short row, short column, short value, bool isGrayedCell)
    {
        Row = row;
        Column = column;
        Value = value;
        IsFixed = value != 0;
        IsGrayedCell = isGrayedCell;
        Domain = GetDomain();
        Removers = new HashSet<Cell>();
    }
    
    private List<short> GetDomain()
    {
        var domain = new List<short>();
        if (Value != 0) return domain;
        
        short min = 1;
        short max = 9;
        short step = 1;
        if (IsGrayedCell)
        {
            min = 2;
            max = 8;
            step = 2;
        }

        for (var i = min; i <= max; i += step)
        {
            domain.Add(i);
        }
        
        return domain;
    }
}