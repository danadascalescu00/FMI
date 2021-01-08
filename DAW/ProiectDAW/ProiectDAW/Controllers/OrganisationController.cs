using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ProiectDAW.Models;

namespace ProiectDAW.Controllers
{
    public class OrganisationController : Controller
    {
        private ApplicationDbContext dbContext = new ApplicationDbContext();

        // GET: Organisation
        public ActionResult Index()
        {
            List<Organisation> organisations = dbContext.Organisations.ToList();
            ViewBag.Organisations = organisations;

            return View();
        }

        public ActionResult Details(int? id)
        {
            if(id.HasValue)
            {
                Organisation organisation = dbContext.Organisations.Find(id);
                if(organisation != null)
                {
                    return View(organisation);
                }
                return HttpNotFound("Couldn't find the organisation with id " + id + "!");
            }
            return HttpNotFound("Missing organisation id parameter!");
        }
    }
}