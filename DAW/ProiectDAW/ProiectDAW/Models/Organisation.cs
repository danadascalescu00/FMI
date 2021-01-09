using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace ProiectDAW.Models
{
    public class Organisation
    {
        public int OrganisationId { get; set; }

        [Required]
        [MinLength(3, ErrorMessage = "The organisation's name  must contain at least 3 characters!")]
        [MaxLength(32, ErrorMessage = "The organisation's name cannot contain more than 32 characters")]
        public string Name { get; set; }

        [Required]
        [MinLength(10, ErrorMessage = "The short description cannot be less than 10 characters!")]
        [MaxLength(250, ErrorMessage = "The short description cannot be more than 200 characters!")]
        public string ShortDescription { get; set; }

        [MinLength(10, ErrorMessage = "The description cannot be less than 10 characters!")]
        [MaxLength(2000, ErrorMessage = "The description cannot be more than 200 characters!")]
        public string Description { get; set; }

        // one-to-one relationship
        public virtual ContactInfo ContactInfo { get; set; }

        // one-to-many relationship
        public virtual ICollection<Project> Projects { get; set; }

        // many-to-many relationship
        public virtual ICollection<Orientation> Orientations { get; set; }

    }
}