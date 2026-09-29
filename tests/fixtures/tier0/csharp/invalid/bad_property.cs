using System;

namespace Mentor.Samples
{
    public class Player
    {
        public string Name { get; set; }
        public int Health { get set; } // expect-error
        public bool IsAlive => Health > 0;
    }
}
