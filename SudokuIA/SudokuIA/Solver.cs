using SudokuIA.Models;

namespace SudokuIA;

public static class Solver
{
    public static void ForwardChecking(SudokuModel model)
    {
        var cellPosition = model.TryGetNextUnfixedCellPosition();
        if (IsSolved(cellPosition))
            return;
        
        var cell = model.Table[cellPosition.Item1, cellPosition.Item2];

        foreach (var value in cell.Domain)
        {
            cell.Value = value;
            cell.IsFixed = true;
            model.UpdateOtherDomains(cell);
            
            if (!model.IsAnyLeftCellWithEmptyDomain())
            {
                ForwardChecking(model);
                if (IsSolved(model.TryGetNextUnfixedCellPosition()))
                    return;
            }
            
            cell.IsFixed = false;
            model.UpdateOtherDomains(cell, true);
            cell.Value = 0;
        }
    }

    public static void MrvChecking(SudokuModel model)
    {
        var cellPosition = model.TryGetNextUnfixedMrvCellPosition();
        if (IsSolved(cellPosition))
            return;
        
        var cell = model.Table[cellPosition.Item1, cellPosition.Item2];

        foreach (var value in cell.Domain)
        {
            cell.Value = value;
            cell.IsFixed = true;
            model.UpdateOtherDomains(cell);
            
            if (!model.IsAnyLeftCellWithEmptyDomain())
            {
                ForwardChecking(model);
                if (IsSolved(model.TryGetNextUnfixedMrvCellPosition()))
                    return;
            }
            
            cell.IsFixed = false;
            model.UpdateOtherDomains(cell, true);
            cell.Value = 0;
        }
    }

    private static bool IsSolved((short, short) cellPosition)
    {
        return cellPosition == (-1, -1);
    }
}