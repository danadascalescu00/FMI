using System;
using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ProiectDAW.Models;
using System.Data.Entity;

namespace ProiectDAW.Controllers
{
    [Authorize(Roles = "Admin")]
    public class UsersController : Controller
    {
        private ApplicationDbContext ctx = new ApplicationDbContext();

        // GET: Users
        public ActionResult Index()
        {
            ViewBag.UsersList = ctx.Users.OrderBy(u => u.UserName).ToList();
            return View();
        }

        public ActionResult Details(string id)
        {
            if (String.IsNullOrEmpty(id))
                return HttpNotFound("Missing user id parameter!");

            ApplicationUser user = ctx.Users.Include("Roles").FirstOrDefault(u => u.Id.Equals(id));
            if(user != null)
            {
                ViewBag.UserRole = ctx.Roles.Find(user.Roles.First().RoleId).Name;
                return View(user);
            }
            return HttpNotFound("Couldn't find the user with id " + id.ToString() + "!");
        }

        [HttpGet]
        public ActionResult Edit(string id)
        {
            if (String.IsNullOrEmpty(id))
                return HttpNotFound("Missing user id parameter!");

            UserViewModel uvm = new UserViewModel();
            uvm.User = ctx.Users.Find(id);
            uvm.RoleName = ctx.Roles.Find(uvm.User.Roles.First().RoleId).Name;
            return View(uvm);
        }

        [HttpPut]
        public ActionResult Edit(string id, UserViewModel uvm)
        {
            try
            {
                ApplicationUser user = ctx.Users.Find(id);

                if(TryUpdateModel(user))
                {
                    var userManager = new UserManager<ApplicationUser>(new UserStore<ApplicationUser>(ctx));
                    foreach(var r in ctx.Roles.ToList())
                    {
                        userManager.RemoveFromRole(user.Id, r.Name);
                    }
                    userManager.AddToRole(user.Id, uvm.RoleName);
                    ctx.SaveChanges();
                }
                return RedirectToAction("Index");
            }catch(Exception e)
            {
                return View(uvm);
            }
        }
    }
}