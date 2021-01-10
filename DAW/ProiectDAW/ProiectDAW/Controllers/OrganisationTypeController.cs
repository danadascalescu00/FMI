using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ProiectDAW.Models;

namespace ProiectDAW.Controllers
{
    public class OrganisationTypeController : Controller
    {
        private ApplicationDbContext dbContext = new ApplicationDbContext();

        // GET: OrganisationType
        public ActionResult Index()
        {
            ViewBag.OrganisationTypes = dbContext.OrganisationTypes.ToList();
            return View();
        }

        public ActionResult New()
        {
            OrganisationType organisationType = new OrganisationType();
            return View(organisationType);
        }

        [HttpPost]
        public ActionResult New(OrganisationType organisationTypeRequest)
        {
            try
            {
                if(ModelState.IsValid)
                {
                    dbContext.OrganisationTypes.Add(organisationTypeRequest);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return View(organisationTypeRequest);
            }
            catch(Exception e)
            {
                return View(organisationTypeRequest);
            }
        }

        public ActionResult Edit(int? id)
        {
            if(id.HasValue)
            {
                OrganisationType organisationType = dbContext.OrganisationTypes.Find(id);
                if(organisationType != null)
                {
                    return View(organisationType);
                }
                return HttpNotFound("Couldn't find this organisation type in database!");
            }
            return HttpNotFound("Missing id parameter!");
        }

        [HttpPut]
        public ActionResult Edit(int id, OrganisationType organisationTypeRequest)
        {
            try
            {
                if(ModelState.IsValid)
                {
                    OrganisationType organisationType = dbContext.OrganisationTypes.Find(id);
                    if(TryUpdateModel(organisationType))
                    {
                        organisationType.Name = organisationTypeRequest.Name;
                        dbContext.SaveChanges();
                    }
                    return RedirectToAction("Index");
                }
                return View(organisationTypeRequest);
            }
            catch(Exception e)
            {
                return View(organisationTypeRequest);
            }
        }

        [HttpDelete]
        public ActionResult Delete(int? id)
        {
            if(id.HasValue)
            {
                OrganisationType organisationType = dbContext.OrganisationTypes.Find(id);
                if(organisationType != null)
                {
                    dbContext.OrganisationTypes.Remove(organisationType);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return HttpNotFound("Couldn't find the organisation type with id " + id.ToString() + "!");
            }
            return HttpNotFound("Missing id parameter!");
        }
    }
}