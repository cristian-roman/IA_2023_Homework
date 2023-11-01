using SudokuIA.Models;

namespace SudokuIA
{
    public static class Entry
    {
        private const string GrayCellFlag = "isGrayCell";
        private const string InstancesPath = @"C:\Users\cristian\[DEV]\IA_2023\IA_2023_First_Homeworks\SudokuIA\SudokuIA\Instances";
        public static void Main(string[] args)
        {
            var instance = LoadInstance("instance_2.txt");
            Console.WriteLine(instance);
            
            Console.WriteLine("\n\n\n\n\n");
            
            Solver.ForwardChecking(instance);
            Console.WriteLine(instance);
        }

        private static SudokuModel LoadInstance(string fileName)
        {
            var table = new Cell[9, 9];
            
            using var reader = new StreamReader(InstancesPath + '\\' + fileName);
            
            for(short row = 0; row < 9; row++)
            for (short column = 0; column < 9; column++)
            {
                var line = reader.ReadLine();
                if (string.IsNullOrEmpty(line))
                {
                    column--;
                    continue;
                }
                var components = line.Split(' ');

                var value = short.Parse(components[0]);
                var isGrayCellFlag = components[1] == GrayCellFlag;

                table[row, column] = new Cell(row, column, value, isGrayCellFlag);
            }

            return new SudokuModel(table);
        }
    }
}

