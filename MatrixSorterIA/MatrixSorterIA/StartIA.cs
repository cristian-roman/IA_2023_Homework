namespace MatrixSorterIA
{
    // ReSharper disable once InconsistentNaming
    internal static class StartIA
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("Case 1:");
            Console.WriteLine("8 6 7 2 5 4 0 3 1");
            Console.WriteLine();
            
            IA.Start(new List<int>()
            {
                8, 6, 7, 2, 5, 4, 0, 3, 1
            });
            
            Console.WriteLine();
            Console.WriteLine("Case 2:");
            Console.WriteLine("2 5 3 1 0 6 4 7 8");
            Console.WriteLine();

            IA.Start(new List<int>()
            {
                2, 5, 3, 1, 0, 6, 4, 7, 8
            });
            
            Console.WriteLine();
            Console.WriteLine("Case 3:");
            Console.WriteLine("2 7 5 0 8 4 3 1 6");
            Console.WriteLine();

            IA.Start(new List<int>
            {
                2, 7, 5, 0, 8, 4, 3, 1, 6
            });
        }
    }
}