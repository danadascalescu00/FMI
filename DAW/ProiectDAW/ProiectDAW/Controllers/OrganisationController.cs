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
            List<Organisation> organisations = dbContext.Organisations.Include("Orientations").ToList();
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

        public ActionResult New()
        {
            Organisation organisation = new Organisation();
            organisation.Orientations = new List<Orientation>();
            return View(organisation);
        }

        [HttpPost]
        public ActionResult New(Organisation organisationRequest)
        {
            try
            {
                if(ModelState.IsValid)
                {
                    dbContext.Organisations.Add(organisationRequest);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return View(organisationRequest);

            }catch(Exception e)
            {
                return View(organisationRequest);
            }
        }

        [HttpGet]
        public ActionResult Edit(int? id)
        {
            if(id.HasValue)
            {
                Organisation organisation = dbContext.Organisations.Find(id);

                if(organisation == null)
                {
                    return HttpNotFound("Couldn't find the organisation with id " + id.ToString() + "!");
                }
                return View(organisation);
            }
            return HttpNotFound("Missing organisation id parameter!");
        }

        [HttpPut]
        public ActionResult Edit(int id, Organisation organisationRequest)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    Organisation organisation = dbContext.Organisations
                                                        .Include("ContactInfo")
                                                        .SingleOrDefault(o => o.OrganisationId.Equals(id));
                    if (TryUpdateModel(organisation))
                    {
                        organisation.Name = organisationRequest.Name;
                        organisation.ShortDescription = organisation.ShortDescription;
                        organisation.Description = organisation.Description;
                        dbContext.SaveChanges();
                    }
                    return RedirectToAction("Index");
                }
                return View(organisationRequest);
            }
            catch (Exception e)
            {
                return View(organisationRequest);
            }
        }

        [HttpDelete]
        public ActionResult Delete(int id)
        {
            Organisation organisation = dbContext.Organisations.Find(id);
            if(organisation != null)
            {
                dbContext.Organisations.Remove(organisation);
                dbContext.SaveChanges();
                return RedirectToAction("Index");
            }
            return HttpNotFound("Couldn't find the organisation with id" + id.ToString() + "!");
        }
    }
}