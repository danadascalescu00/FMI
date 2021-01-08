using System.Data.Entity;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;

namespace ProiectDAW.Models
{
    // You can add profile data for the user by adding more properties to your ApplicationUser class, please visit https://go.microsoft.com/fwlink/?LinkID=317594 to learn more.
    public class ApplicationUser : IdentityUser
    {
        public async Task<ClaimsIdentity> GenerateUserIdentityAsync(UserManager<ApplicationUser> manager)
        {
            // Note the authenticationType must match the one defined in CookieAuthenticationOptions.AuthenticationType
            var userIdentity = await manager.CreateIdentityAsync(this, DefaultAuthenticationTypes.ApplicationCookie);
            // Add custom user claims here
            return userIdentity;
        }
    }

    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext()
            : base("DefaultConnection", throwIfV1Schema: false)
        {
            Database.SetInitializer<ApplicationDbContext>(new Initp());
        }

        public DbSet<Organisation> Organisations { get; set; }
        public DbSet<ContactInfo> ContactInfos { get; set; }

        public static ApplicationDbContext Create()
        {
            return new ApplicationDbContext();
        }
    }

    public class Initp : DropCreateDatabaseAlways<ApplicationDbContext>
    {
        protected override void Seed(ApplicationDbContext context)
        {
            ContactInfo contactInfo1 = new ContactInfo
            {
                Email = "asociatia@tasuleasasocial.ro",
                PhoneNumber = "+40 758 745 767"
            };

            ContactInfo contactInfo2 = new ContactInfo
            {
                Email = "aiesec@aiesec.ro"
            };

            context.ContactInfos.Add(contactInfo1);
            context.ContactInfos.Add(contactInfo2);

            Organisation organisation1 = new Organisation
            {
                Name = "Tasuleasa Social",
                ShortDescription = "We set out to change the mindsets of those around us." +
                 "and to show that young people want to get involved in solving social problems.",
                Description = "For the Tășuleasa Social Association, the most important values are volunteering, " +
                "respect for nature, educating young people through practical examples and developing civic courage " +
                "among young people through their involvement in social and environmental issues.",
                ContactInfo = contactInfo1
            };
            
            Organisation organisation2 = new Organisation
            {
                Name = "AIESEC",
                ShortDescription = "We are a youth leadership movement." +
                " We are passionately driven by one cause, peace and fulfillment of humankind's potential.",
                Description = "AIESEC is a non-governmental not-for-profit organisation in consultative status with " +
                "the United Nations Economic and Social Council (ECOSOC), affiliated with the UN DPI, member of " +
                "ICMYO, and is recognized by UNESCO. AIESEC International Inc. is registered as a Not-for-profit " +
                "Organisation under the Canadian Not-for-profit Corporations Act - 2018-02-08, Corporation Number: " +
                "1055154-6 and Quebec Business Number (NEQ) 1173457178 in Montreal, Quebec, Canada.",
                ContactInfo = contactInfo2
            };            
            
           Organisation organisation3 = new Organisation
            {
                Name = "Cercetașii României",
                ShortDescription = "National Organisation \"Cercetașii României\" is the main scout organization in Romania.",
                Description = "Scouting is an international youth movement created to help " +
                "young people in their physical, mental and spiritual development, to become constructive members of society. "
           };

            context.Organisations.Add(organisation1);
            context.Organisations.Add(organisation2);
            context.Organisations.Add(organisation3);

            context.SaveChanges();
            base.Seed(context);
        }
    }
}