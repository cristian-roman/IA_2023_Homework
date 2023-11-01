using System.Diagnostics;
using SudokuIA.Models;

namespace SudokuIA
{
    public static class Entry
    {
        private const string GrayCellFlag = "isGrayCell";
        private const string InstancesPath = @"C:\Users\cristian\[DEV]\IA_2023\IA_2023_First_Homeworks\SudokuIA\SudokuIA\Instances";
        public static void Main(string[] args)
        {
            var forwardCheckingInstance = LoadInstance("instance_1.txt");
            Console.WriteLine(forwardCheckingInstance);
            
            Console.WriteLine("\n\n\n\n\n");
            
            var stopwatch = new Stopwatch();
            
            
            stopwatch.Start();
            Solver.ForwardChecking(forwardCheckingInstance);
            stopwatch.Stop();
            Console.WriteLine("[Forward checking] Solved instance: " + stopwatch.ElapsedMilliseconds + " ms");
            Console.WriteLine(forwardCheckingInstance);
            
            Console.WriteLine("\n\n\n\n\n");
            
            var mrvCheckingInstance = LoadInstance("instance_1.txt");
            stopwatch.Reset();
            stopwatch.Start();
            Solver.MrvChecking(mrvCheckingInstance);
            stopwatch.Stop();
            Console.WriteLine("[MRV checking] Solved instance: " + stopwatch.ElapsedMilliseconds + " ms");
            Console.WriteLine(mrvCheckingInstance);
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

