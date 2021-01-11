using ProiectDAW.Models.MyValidator;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace ProiectDAW.Models
{
    public class Organisation
    {
        [Index("OrganisationId_Index", 1)]
        public int OrganisationId { get; set; }

        [Required]
        [MinLength(3, ErrorMessage = "The organisation's name  must contain at least 3 characters!")]
        [MaxLength(32, ErrorMessage = "The organisation's name cannot contain more than 32 characters")]
        public string Name { get; set; }

        [Required]
        [Display(Name="Registration Date")]
        [RegularExpression(@"^((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))[- /.]((0[1-9]|1[012]))[- /.](19|20)\d\d$",
            ErrorMessage = "This is not a valid date! \nValid date formats: dd/mm/yyyy  dd.mm.yyyy dd-mm-yy")]
        public string RegistrationDate { get; set; }

        [Column(TypeName = "VARCHAR")]
        [StringLength(50)]
        [Index("RegistrationCode_Index", 2, IsUnique = true)]
        public string RegistrationCode { get; set; }

        [Required]
        [MinLength(10, ErrorMessage = "The short description cannot be less than 10 characters!")]
        [MaxLength(250, ErrorMessage = "The short description cannot be more than 200 characters!")]
        public string ShortDescription { get; set; }

        [MinLength(10, ErrorMessage = "The description cannot be less than 10 characters!")]
        [MaxLength(2000, ErrorMessage = "The description cannot be more than 200 characters!")]
        public string Description { get; set; }

        // one-to-one relationship
        public virtual ContactInfo ContactInfo { get; set; }

        // many-to-one relationship
        [ForeignKey("OrganisationRefId")]
        public virtual ICollection<Project> Projects { get; set; }

        // many-to-many relationship
        public virtual ICollection<Orientation> Orientations { get; set; }

        // one-to-many
        public int OrganisationTypeId { get; set; }

        [ForeignKey("OrganisationTypeId")]
        public virtual OrganisationType OrganisationType { get; set; }

        // checkboxes list
        [NotMapped]
        public List<CheckBoxViewModel> OrientationsList { get; set; }

        [NotMapped]
        public IEnumerable<SelectListItem> OrganisationTypeList { get; set; }

    }
}