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

        public static ApplicationDbContext Create()
        {
            return new ApplicationDbContext();
        }
    }

    public class Initp : DropCreateDatabaseAlways<ApplicationDbContext>
    {
        protected override void Seed(ApplicationDbContext context)
        {
            Organisation organisation1 = new Organisation
            {
                OrganisationId = "E12332145",
                Name = "Tasuleasa Social",
                ShortDescription = "Ne-am propus să schimbăm mentalitățile celor din jurul nostru " +
                "și să arătăm că tinerii doresc să se implice în rezolvarea problemelor sociale."
            };
            
            Organisation organisation2 = new Organisation
            {
                OrganisationId = "E12332146",
                Name = "AIESEC",
                ShortDescription = "We are a youth leadership movement." +
                " We are passionately driven by one cause, peace and fulfillment of humankind's potential."
            };            
            
            Organisation organisation3 = new Organisation
            {
                OrganisationId = "E18932146",
                Name = "WWFRomania",
                ShortDescription = "În România, WWF lucrează din anul 2006 pentru protejarea mediului sălbatic din " +
                "Munții Carpați și din lungul Dunării: arii protejate, păduri, urși bruni, zimbri, Delta Dunării, " +
                "sturioni. La toate acestea se adaugă stimularea tranziției spre economia verde și un program de " +
                "educație de mediu adresat tinerilor."
            };            
            
           Organisation organisation4 = new Organisation
            {
                OrganisationId = "E12339046",
                Name = "Cercetașii României",
                ShortDescription = "Cercetășia este o mișcare internațională de tineri creată cu scopul de a ajuta " +
                "tinerii în dezvoltarea lor fizică, mentală și spirituală, pentru a deveni membri constructivi ai societății. "
           };

            context.Organisations.Add(organisation1);
            context.Organisations.Add(organisation2);
            context.Organisations.Add(organisation3);
            context.Organisations.Add(organisation4);

            context.SaveChanges();
            base.Seed(context);
        }
    }
}