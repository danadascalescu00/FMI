using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(ProiectDAW.Startup))]
namespace ProiectDAW
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
