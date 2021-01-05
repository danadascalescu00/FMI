using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using Microsoft.Owin;
using Owin;
using ProiectDAW.Models;

[assembly: OwinStartupAttribute(typeof(ProiectDAW.Startup))]
namespace ProiectDAW
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
            CreateAdminAndUserRoles();
        }

        private void CreateAdminAndUserRoles()
        {
            var ctx = new ApplicationDbContext();
            var roleManager = new RoleManager<IdentityRole>(new RoleStore<IdentityRole>(ctx));
            var userManager = new UserManager<ApplicationUser>(new UserStore<ApplicationUser>(ctx));
            
            // add the roles that a user can have within the application
            if(!roleManager.RoleExists("Admin"))
            {
                // add Admin role
                var role = new IdentityRole();
                role.Name = "Admin";
                roleManager.Create(role);

                // add admin user
                var user = new ApplicationUser();
                user.UserName = "danadascalescu00@gmail.com";
                user.Email = "danadascalescu00@gmail.com";

                var adminCreated = userManager.Create(user, "Admin2020");
                if(adminCreated.Succeeded)
                {
                    userManager.AddToRole(user.Id, "Admin");
                }
            }
        }
    }
}
