using System.Text;

namespace SudokuIA.Models;

public class SudokuModel
{
    public Cell[,] Table { get; set; }
    
    public SudokuModel()
    {
        Table = new Cell[9, 9];
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