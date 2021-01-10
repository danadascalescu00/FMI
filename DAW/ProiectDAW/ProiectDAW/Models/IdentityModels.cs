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
                ShortDescription = "\"Școala de Mers pe Munte\" is a project for adults in Romania and the Republic " +
                    "of Moldova, in which theoretical and practical knowledge is presented in a structured way. " +
                    "The project contributes, in this way, to capitalizing on the tourist potential of the area: " +
                    "the Călimani Mountains welcome tourists with spectacular places and landscapes, with a national" +
                    " park, a wide network of tourist routes and welcoming locals.",
                Description = "Școala de Mers pe Munte teaches you to listen to the mountain! The project continues for" +
                    "for the 5th consecutive year with 8 more groups. We will select 200 people and we will go " +
                    "together on the mountain at over 2000m altitude. In the 4 editions, 1000 beginners \"graduated\"" +
                    " the project courses, and most characterized the school as follows: inspirational, educational, " +
                    "extraordinary, emotional, full of energy or friendly."
            };

            Project project2 = new Project
            {
                Name = "Camionul de Craciun",
                ShortDescription = "We started by giving gifts to needy children in the early years, then gradually " +
                "turned into an educational action, through which thousands of children learned to receive, " +
                "to pass on and especially to do something for the community and the place in which they live " +
                "through projects conceived by them.",
                Description = "The Tasuleasa Social Association has grown a lot with this action, and now at the 15th " +
                    "edition it will be the biggest Truck we have ever organized, 25,191 children that we will visit, " +
                    "that is 21 trucks." + System.Environment.NewLine + " We started by giving gifts to needy children in " +
                    "the early years, then gradually turned into an educational action, through which thousands of " +
                    "children learned to receive, to pass on and especially to do something for the community and the" +
                    " place. in which they live through projects conceived by them. " +
                    "This is how \"Good day!\" Little Volunteers' Day\" which is eagerly awaited by them as the " +
                    "Christmas Truck. This year, the Trucks will go on December 28 and 29 in 5 counties, where in" +
                    " addition to Tasuleasa Social volunteers, numerous educators, teachers, professors, gendarmes," +
                    " firefighters and police will be volunteers of the Christmas Truck in an excellent model of " +
                    "collaboration.One of the trucks will go in January to the Republic of Moldova to Glodeni, " +
                    "a district twinned with Bistrita - Nasaud County."
            };

            Project project3 = new Project
            {
                Name = "Via Maria Theresia",
                ShortDescription = "The Via Maria Theresia project is designed as an example of good practice " +
                "for mountain competitions. The route has a length of 42,195 km and will remain a constant marathon, " +
                "mountain biking and hiking, open in summer or winter, day or night, for all those interested.",
                Description = "Via Maria Theresia is a historic road located in the Călimani mountains, built " +
                    "hundreds of years ago, in order to support the border guard troops of the Austro-Hungarian Empire " +
                    "with weapons and food." + System.Environment.NewLine + System.Environment.NewLine +
                    "Currently, Maria Theresia's road partially overlaps with a rather poorly signposted tourist " +
                    "route, therefore very rarely traveled by tourists. The few hikers who dare to cross it do not " +
                    "know that their road, which connects Bistrița-Năsăud County with Suceava County, once connected " +
                    "Transylvania with Bucovina."
            };

            //Project project4 = new Project
            //{
                //Name = "Pădurea Transilvania 7.0",
              //  ShortDescription = "Așteptată cu nerăbdare de mulți, pregătim acțiunea de plantare Pădurea " +
            //        "Transilvania 5.0! Banca Transilvania, partenerul nostru de cursă lungă în acțiuni de împădurire " +
            //        "ne însoțit din nou la o plantare marca Pădurea Transilvania, adică mare, de 10 hectare. " + System.Environment.NewLine +
            //        "Locul activității este unul cunoscut deja veteranilor de plantare cu Tășu, și anume Sânmihaiu de Câmpie, județul Bistrița - Năsăud."
            //};

            context.Projects.Add(project1);
            context.Projects.Add(project2);
            context.Projects.Add(project3);
            //context.Projects.Add(project4);


            Organisation organisation1 = new Organisation
            {
                Name = "Tasuleasa Social",
                ShortDescription = "We set out to change the mindsets of those around us." +
                 "and to show that young people want to get involved in solving social problems.",
                Description = "For the Tășuleasa Social Association, the most important values are volunteering, " +
                "respect for nature, educating young people through practical examples and developing civic courage " +
                "among young people through their involvement in social and environmental issues.",
                ContactInfo = contactInfo1,
                Projects = new List<Project> { project1, project2, project3 },
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