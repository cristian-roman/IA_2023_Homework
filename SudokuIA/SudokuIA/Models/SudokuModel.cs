namespace SudokuIA.Models;

public class SudokuModel
{
    public Cell[,] Table { get; set; }
    
    public SudokuModel()
    {
        Table = new Cell[9, 9];
    }
}