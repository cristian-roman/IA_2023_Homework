using System.Text;

namespace SudokuIA.Models;

public class SudokuModel
{
    public Cell[,] Table { get; }

    private readonly Dictionary<(short, short), List<short>> _domains;

    public SudokuModel(Cell[,] table)
    {
        Table = table;
        _domains = new Dictionary<(short,short), List<short>>();

        for (short i = 0; i < 9; i++)
        for (short j = 0; j < 9; j++)
        {
            var cell = Table[i, j];
            _domains.Add((cell.Row, cell.Column), cell.Domain);
        }
        
        FineTuneDomains();
    }

    private void FineTuneDomains()
    {
        for (short i = 0; i < 9; i++)
        for (short j = 0; j < 9; j++)
        {
            var cell = Table[i, j];
            if (cell.IsFixed)
            {
                UpdateOtherDomains(cell);
            }
        }
    }

    public void UpdateOtherDomains(Cell cell, bool isUndo = false)
    {
        UpdateRow(cell, isUndo);
        UpdateColumn(cell, isUndo);
        UpdateInternalSquare(cell, isUndo);
    }

    private void UpdateRow(Cell cell, bool isUndo = false)
    {
        for (short column = 0; column < 9; column++)
        {
            if (column == cell.Column || Table[cell.Row, column].IsFixed) continue;

            if (isUndo)
            {
                if (!Table[cell.Row, column].Removers.Contains(cell)) continue;
                
                _domains[(cell.Row, column)].Add(cell.Value);
                Table[cell.Row, column].Removers.Remove(cell);
            }
            else if (_domains[(cell.Row, column)].Remove(cell.Value))
            {
                Table[cell.Row, column].Removers.Add(cell);
            }
        }
    }
    
    private void UpdateColumn(Cell cell, bool isUndo = false)
    {
        for(short row = 0; row < 9; row++)
        {
            if (row == cell.Row || Table[row, cell.Column].IsFixed) continue;

            if (isUndo)
            {
                if (!Table[row, cell.Column].Removers.Contains(cell)) continue;
                
                _domains[(row, cell.Column)].Add(cell.Value);
                Table[row, cell.Column].Removers.Remove(cell);
            }
            else if (_domains[(row, cell.Column)].Remove(cell.Value))    
            {
                Table[row, cell.Column].Removers.Add(cell);
            }
        }
    }

    private void UpdateInternalSquare(Cell cell, bool isUndo = false)
    {
        var rowStart = (short) (cell.Row / 3 * 3);
        var columnStart = (short) (cell.Column / 3 * 3);
        
        for (var i = rowStart; i < rowStart + 3; i++)
            for (var j = columnStart; j < columnStart + 3; j++)
            {
                if ((i == cell.Row && j == cell.Column) || Table[i,j].IsFixed) continue;
                
                if (isUndo)
                {
                    if (!Table[i,j].Removers.Contains(cell)) continue;
                    
                    _domains[(i,j)].Add(cell.Value);
                    Table[i,j].Removers.Remove(cell);
                }
                else if (_domains[(i,j)].Remove(cell.Value))
                    Table[i,j].Removers.Add(cell);
            }
    }
    
    public bool IsAnyLeftCellWithEmptyDomain()
    {
        for (short i = 0; i < 9; i++)
        for (short j = 0; j < 9; j++)
        {
            if (!Table[i,j].IsFixed && _domains[(i, j)].Count == 0)
            {
                return true;
            }
        }

        return false;
    }

    public (short, short) TryGetNextUnfixedCellPosition()
    {
        for (short row = 0; row < 9; row++)
        for (short column = 0; column < 9; column++)
        {
            if (!Table[row, column].IsFixed)
            {
                return (row, column);
            }
        }
        
        return (-1, -1);
    }
    
    public (short,short) TryGetNextUnfixedMrvCellPosition()
    {
        var numberOfOccurrences = 100;
        var ans = ((short)-1, (short)-1);
        
        for (short row = 0; row < 9; row++)
        for (short column = 0; column < 9; column++)
        {
            if (Table[row, column].IsFixed) continue;
            if (_domains[(row, column)].Count >= numberOfOccurrences) continue;
            
            numberOfOccurrences = _domains[(row, column)].Count;
            ans = (row, column);
        }
        
        return ans;
    }
    public override string ToString()
    {
        var sb = new StringBuilder();

        for (var i = 0; i < 9; i++)
        {
            for (var j = 0; j < 9; j++)
            {
                var cell = Table[i, j];

                if (cell.IsGrayedCell)
                {
                    sb.Append('\u001b');
                    sb.Append("[48;5;8m");
                }

                sb.Append(cell.Value);

                if (cell.IsGrayedCell)
                {
                    sb.Append('\u001b');
                    sb.Append("[0m");
                }

                if (j % 3 == 2 && j != 8)
                {
                    sb.Append('|'); // Add vertical bar after every third column (excluding the last column)
                }

                sb.Append(' ');
            }
        
            sb.Append('\n');

            if (i % 3 == 2 && i != 8)
            {
                sb.Append("-----+------+------\n"); // Add horizontal line after every third row (excluding the last row)
            }
        }

        return sb.ToString();
    }
}