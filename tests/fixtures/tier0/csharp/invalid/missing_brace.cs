using System;

namespace Mentor.Samples
{
    public class Counter
    {
        private int value;

        public void Increment()
        {
            value++;
        }

        public int Value => value; // expect-error
