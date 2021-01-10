using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ProiectDAW.Models
{
    public class OrganisationType
    {
        public int OrganisationTypeId { get; set; }
        public string Name { get; set; }

        // many-to-one
        public virtual ICollection<Organisation> Organisations { get; set; }
    }
}