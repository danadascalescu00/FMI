using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ProiectDAW.Models;

namespace ProiectDAW.Controllers
{
    public class OrientationController : Controller
    {
        private ApplicationDbContext dbContext = new ApplicationDbContext();

        // GET: Orientation
        public ActionResult Index()
        {
            ViewBag.Orientations = dbContext.Orientations.ToList();
            return View();
        }

        [HttpGet]
        public ActionResult New()
        {
            Orientation orientation = new Orientation();
            return View(orientation);
        }

        [HttpPost]
        public ActionResult New(Orientation orientation)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    dbContext.Orientations.Add(orientation);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return View(orientation);
            }
            catch (Exception e)
            {
                return View(orientation);
            }
        }

        public ActionResult Edit(int? id)
        {
            if (id.HasValue)
            {
                Orientation orientation = dbContext.Orientations.Find(id);
                if (orientation != null)
                {
                    return View(orientation);
                }
                return HttpNotFound("Couldn't find this organisation type in database!");
            }
            return HttpNotFound("Missing id parameter!");
        }

        [HttpPut]
        public ActionResult Edit(int id, Orientation orientationRequest)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    Orientation orientation = dbContext.Orientations.Find(id);
                    if (TryUpdateModel(orientation))
                    {
                        orientation.Name = orientationRequest.Name;
                        dbContext.SaveChanges();
                    }
                    return RedirectToAction("Index");
                }
                return View(orientationRequest);
            }
            catch (Exception e)
            {
                return View(orientationRequest);
            }
        }

        [HttpDelete]
        public ActionResult Delete(int? id)
        {
            if (id.HasValue)
            {
                Orientation orientation = dbContext.Orientations.Find(id);
                if (orientation != null)
                {
                    dbContext.Orientations.Remove(orientation);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return HttpNotFound("Couldn't find the orientation type with id " + id.ToString() + "!");
            }
            return HttpNotFound("Missing id parameter!");
        }
    }
}