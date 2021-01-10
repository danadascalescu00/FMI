using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ProiectDAW.Models;

namespace ProiectDAW.Models
{
    public class Project
    {
        public int ProjectId { get; set; }

        [Required]
        public string Name { get; set; }

        [Required]
        [MinLength(10, ErrorMessage = "The short description cannot be less than 10 characters!")]
        [MaxLength(500, ErrorMessage = "The short description cannot be more than 200 characters!")]
        public string ShortDescription { get; set; }

        [MinLength(10, ErrorMessage = "The description cannot be less than 10 characters!")]
        [MaxLength(2500, ErrorMessage = "The description cannot be more than 200 characters!")]
        public string Description { get; set; }

        public IEnumerable<SelectListItem> OrganisationList { get; set; }

        // many-to-one relationship
        [Column("Organisation_Id")]
        public int OrganisationRefId { get; set; }
        public virtual Organisation Organisation { get; set; }
    }
}