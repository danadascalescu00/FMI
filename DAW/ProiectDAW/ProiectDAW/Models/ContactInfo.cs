using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data;
using System.Linq;
using System.Web;

namespace ProiectDAW.Models
{
    [Table("Contacts")]
    public class ContactInfo
    {
        public int ContactInfoId { get; set; }
        [RegularExpression(@"^[+]\(?([0-9]{2})\)?[-. ]?([0-9]{3})?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$",
            ErrorMessage = "This is not a valid phone number")]
        public string PhoneNumber { get; set; }

        [RegularExpression(@"^[\w!#$%&'*+\-/=?\^_`{|}~]+(\.[\w!#$%&'*+\-/=?\^_`{|}~]+)*@((([\-\w]+\.)+[a-zA-Z]{2,4})|(([0-9]{1,3}\.){3}[0-9]{1,3}))$",
            ErrorMessage = "This is not a valid email address")]
        public string Email { get; set; }

        // one-to-one relationship
        [Required]
        public virtual Organisation Organisation { get; set; }
    }
}