namespace SudokuIA.Models;

public class Cell
{
    public short Value;

    public bool IsFixed => _possibleValues.Count == 1;
    public readonly bool IsGrayedCell;
    private readonly List<short> _possibleValues;
    private short _currentIndex;
    public Cell(short value, bool isGrayCell)
    {
        Value = value;
        _possibleValues = new List<short>();
        IsGrayedCell = isGrayCell;
        if (Value == 0)
        {
            short min = 1;
            short max = 9;
            short step = 1;
            if (isGrayCell)
            {
                min = 2;
                max = 8;
                step = 2;
            }
            
            for (var i = min; i <= max; i += step)
            {
                _possibleValues.Add(i);
            }
        }
        else if (Value is < 0 or > 9)
        {
            throw new Exception("Invalid value");
        }
        else
        {
            _possibleValues = new List<short> {Value};
        }

        _currentIndex = 0;
    }
    
    public void SetNextValueIterative()
    {
        _currentIndex = (short) ((_currentIndex+1) % _possibleValues.Count);
        Value = _possibleValues[_currentIndex];
    }
}