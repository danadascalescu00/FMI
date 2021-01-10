using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using System.Web;
using ProiectDAW.Models;
using System.ComponentModel.DataAnnotations;

namespace ProiectDAW.Models.MyValidator
{
    public class RegistrationCodeValidator : ValidationAttribute
    {
        private bool IsUnique(string registrationCode)
        {
            if (!String.IsNullOrEmpty(registrationCode))
            {
                ApplicationDbContext dbContext = new ApplicationDbContext();
                return dbContext.Organisations.FirstOrDefault(o => o.RegistrationCode == registrationCode) == null;
            }
            return false;
        }

        private ValidationResult validateRegistrationCode(string registrationCode, string registrationDate)
        {
            if (registrationCode == null)
                return new ValidationResult("Registration code(PIC) field is required!");

            if (registrationCode.Length != 11)
                return new ValidationResult("Registration code(PIC) must contain 11 characters!");

            Regex regex = new Regex(@"^E\d{10}$");
            if (!regex.IsMatch(registrationCode))
                return new ValidationResult("This is not a valid format for registration code(PIC)!");

            //if (!IsUnique(registrationCode))
              //  return new ValidationResult("Registration code(PIC) must be unique!");

            string dd = registrationCode.Substring(1, 2);
            string mm = registrationCode.Substring(3, 2);
            string yy = registrationCode.Substring(5, 2);
            string sss = registrationCode.Substring(7, 3);
            char c = registrationCode.ElementAt(10);

            string day = registrationDate.Substring(0, 2);
            if (!dd.Equals(day))
                return new ValidationResult("DD component is not valid!");

            string month = registrationDate.Substring(3, 2);
            if (!mm.Equals(month))
                return new ValidationResult("MM component is not valid!");

            string year = registrationDate.Substring(8, 2);
            if (!yy.Equals(year))
                return new ValidationResult("YY component is not valid!");

            regex = new Regex(@"^((00[1-9])|(0[1-9]\d)|([1-9]\d\d))$");
            if (!regex.IsMatch(sss))
                return new ValidationResult("SSS component is not valid!");

            return ValidationResult.Success;
        }

        protected override ValidationResult IsValid(object value, ValidationContext validationContext)
        {
            Organisation organisation = (Organisation)validationContext.ObjectInstance;
            return validateRegistrationCode(organisation.RegistrationCode, organisation.RegistrationDate);
        }
    }
}