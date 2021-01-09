using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ProiectDAW.Models
{
    public class Orientation
    {
        public int OrientationId { get; set; }
        public string Name { get; set; }

        // many-to-many relationship
        public virtual ICollection<Orientation> orientations { get; set; }
    }
}