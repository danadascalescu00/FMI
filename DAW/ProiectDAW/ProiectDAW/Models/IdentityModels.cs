using System.Collections.Generic;
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
        public DbSet<Project> Projects { get; set; }
        public DbSet<Orientation> Orientations { get; set; }
        public DbSet<OrganisationType> OrganisationTypes { get; set; }

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

            context.ContactInfos.Add(contactInfo1);

            Orientation orientation1 = new Orientation { Name = "Charities" };
            Orientation orientation2 = new Orientation { Name = "Service" };
            Orientation orientation3 = new Orientation { Name = "Participation" };
            Orientation orientation4 = new Orientation { Name = "Empowerment" };

            context.Orientations.Add(orientation1);
            context.Orientations.Add(orientation2);
            context.Orientations.Add(orientation3);
            context.Orientations.Add(orientation4);

            OrganisationType organisationType1 = new OrganisationType { OrganisationTypeId = 10, Name = "Comunity Based" };
            OrganisationType organisationType2 = new OrganisationType { OrganisationTypeId = 11, Name = "City Wide" };
            OrganisationType organisationType3 = new OrganisationType { OrganisationTypeId = 12, Name = "Regional" };
            OrganisationType organisationType4 = new OrganisationType { OrganisationTypeId = 13, Name = "National" };
            OrganisationType organisationType5 = new OrganisationType { OrganisationTypeId = 14, Name = "International" };

            context.OrganisationTypes.Add(organisationType1);
            context.OrganisationTypes.Add(organisationType2);
            context.OrganisationTypes.Add(organisationType3);
            context.OrganisationTypes.Add(organisationType4);
            context.OrganisationTypes.Add(organisationType5);

            Project project1 = new Project
            {
                Name = "Școala de mers pe munte",
                ShortDescription = "Școala de Mers pe Munte este un proiect destinat persoanelor adulte din România " +
                    "și Republica Moldova, în cadrul căruia se prezintă cunoştinţe teoretice și practice în mod " +
                    "structurat. Proiectul contribuie, în acest fel, la valorificarea potenţialului turistic al zonei: " +
                    "Munţii Călimani îi întâmpinã pe turişti cu locuri şi peisaje spectaculoase, cu un parc naţional, " +
                    "o amplă reţea de trasee turistice şi localnici primitori.",
                Description = "Școala de Mers pe Munte te învață să asculți muntele! Proiectul continuă pentru " +
                    "al 5-lea an consecutiv cu încă 8 grupe. Vom selecta 200 de persoane și vom merge împreună pe munte " +
                    "la peste 2000m altitudine. În cele 4 ediții desfășurate, 1000 de persoane începătoare au " +
                    "˝absolvit˝ cursurile proiectului, iar majoritatea au caracterizat școala astfel : inspirațională, " +
                    "educativă, extraordinară, emoționantă, plină de energie sau prietenoasă."
            };

            context.Projects.Add(project1);


            Organisation organisation1 = new Organisation
            {
                Name = "Tasuleasa Social",
                ShortDescription = "We set out to change the mindsets of those around us." +
                 "and to show that young people want to get involved in solving social problems.",
                Description = "For the Tășuleasa Social Association, the most important values are volunteering, " +
                "respect for nature, educating young people through practical examples and developing civic courage " +
                "among young people through their involvement in social and environmental issues.",
                ContactInfo = contactInfo1,
                Projects = new List<Project> { project1 },
                Orientations = new List<Orientation> { orientation1, orientation2, orientation3 },
                OrganisationTypeId = organisationType4.OrganisationTypeId
            };
            
            
           Organisation organisation3 = new Organisation
            {
                Name = "Cercetașii României",
                ShortDescription = "National Organisation \"Cercetașii României\" is the main scout organization in Romania.",
                Description = "Scouting is an international youth movement created to help " +
                    "young people in their physical, mental and spiritual development, to become constructive members of society.",
                Orientations = new List<Orientation> { orientation3, orientation4 },
                OrganisationTypeId = organisationType4.OrganisationTypeId
           };

            Organisation organisation4 = new Organisation
            {
                Name = "WWF Romania",
                ShortDescription = "The World Wide Fund for Nature is a non-governmental organization for nature " +
                    "conservation and ecological restoration of the natural environment.",
                Description = "Suntem cu toții conectați la ADN-ul planetei. Natura este sursa noastră fundamentală " +
                    "pentru viață. Dar, în prezent, se degradează într-un ritm accelerat și noi, oamenii, suntem " +
                    "responsabili pentru această situație: populațiile de specii sălbatice s-au înjumătățit în doar " +
                    "40 de ani, la fel s-a redus și calitatea râurilor și a pădurilor. Efectele dezastruoase ale " +
                    "schimbărilor climatice sunt din ce în ce mai vizibile – fenomene meteo extreme, care cauzează " +
                    "dezastre naturale, lasă comunități întregi fără apă de băut, hrană și adapost, forțând din ce" +
                    " în ce mai mulți oameni să migreze." + System.Environment.NewLine +
                    "Modul în care trăim pune o presiune mult prea mare pe natură: consumăm mai mult decât " +
                    "natura ne poate oferi într - un an, consumăm resursele naturale mai repede decât acestea se pot " +
                    "regenera. Viața noastră devine astfel din ce în ce mai nesigură și nesănătoasă, iar bunăstarea," +
                    " sănătatea, dezvoltarea generațiilor viitoare este pusa în pericol." + System.Environment.NewLine +
                    " De aceea ne propunem să oprim degradarea Planetei, protejând biodiversitata – " +
                    "toate speciile si ecosistemele care fac Pâmântul locuibil pentru oameni. Ne propunem " +
                    "să construim un viitor în care oamenii trăiesc și se dezvoltă în armonie cu natura. " +
                    "Dacă vom acea succes, în 30 de ani declinul naturii va fi oprit; ecosistemele vor fi " +
                    "reziliente și vor exista mecanisme sociale, economice și politice care să asigure folosirea " +
                    "responsabilă a resurselor, iar poluarea va fi redusă în limite sigure pentru viață.",
                Orientations = new List<Orientation> { orientation1, orientation4 },
                OrganisationTypeId = organisationType4.OrganisationTypeId
            };

            context.Organisations.Add(organisation1);
            context.Organisations.Add(organisation3);
            context.Organisations.Add(organisation4);

            context.SaveChanges();
            base.Seed(context);
        }
    }
}