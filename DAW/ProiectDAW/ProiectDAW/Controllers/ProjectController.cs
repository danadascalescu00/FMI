using System;
using System.Collections.Generic;
using System.Linq;
using System.Web; 
using System.Web.Mvc;
using ProiectDAW.Models;

namespace ProiectDAW.Controllers
{
    public class ProjectController : Controller
    {
        private ApplicationDbContext dbContext = new ApplicationDbContext();

        // GET: Project
        public ActionResult Index()
        {
            List<Project> projects = dbContext.Projects.Include("Organisation").ToList();
            ViewBag.Projects = projects;
            return View();
        }

        public ActionResult Details(int? id)
        {
            if(id.HasValue)
            {
                Project project = dbContext.Projects.Find(id);
                if(project != null)
                {
                    return View(project);
                }
                return HttpNotFound("Couldn't find the project with id" + id.ToString() + "!");

            }
            return HttpNotFound("Missing project id parameter!");
        }

        public ActionResult New()
        {
            Project project = new Project();
            project.OrganisationList = GetAllOrganisations();
            return View(project);
        }

        [HttpPost]
        public ActionResult New(Project projectRequest)
        {
            try
            {
                projectRequest.OrganisationList = GetAllOrganisations();
                if (ModelState.IsValid)
                {
                    dbContext.Projects.Add(projectRequest);
                    dbContext.SaveChanges();
                    return RedirectToAction("Index");
                }
                return View(projectRequest);
            }
            catch (Exception e)
            {
                return View(projectRequest);
            }
        }

        public ActionResult Edit(int? id)
        {
            if(id.HasValue)
            {
                Project project = dbContext.Projects.Find(id);
                if(project == null)
                {
                    return HttpNotFound("Couldn't find the project with id " + id.ToString() + "!");
                }

                project.OrganisationList = GetAllOrganisations();
                return View(project);
            }
            return HttpNotFound("Missing project id parameter!");
        }

        [HttpPut]
        public ActionResult Edit(int id, Project projectRequest)
        {
            try
            {
                projectRequest.OrganisationList = GetAllOrganisations();
                if(ModelState.IsValid)
                {
                    Project project = dbContext.Projects.Include("Organisation")
                                                        .SingleOrDefault(p => p.ProjectId.Equals(id));

                    if(TryUpdateModel(project))
                    {
                        project.Name = projectRequest.Name;
                        project.ShortDescription = projectRequest.ShortDescription;
                        project.Description = projectRequest.Description;
                        dbContext.SaveChanges();
                    }
                    return RedirectToAction(actionName: "Details", controllerName: "Project", routeValues: new { id = project.ProjectId });
                }
                return View(projectRequest);

            }
            catch(Exception e)
            {
                return View(projectRequest);
            }
        }

        [HttpDelete]
        public ActionResult Delete(int id)
        {
            Project project = dbContext.Projects.Find(id);
            if(project != null)
            {
                dbContext.Projects.Remove(project);
                dbContext.SaveChanges();
                return RedirectToAction(actionName: "Details", controllerName: "Organisation", routeValues: new { id = project.OrganisationRefId });
            }
            return HttpNotFound("Couldn't find the project with " + id.ToString() + "!");
        }

        [NonAction]
        public IEnumerable<SelectListItem> GetAllOrganisations()
        {
            var selectedList = new List<SelectListItem>();
            foreach(var organisation in dbContext.Organisations.ToList())
            {
                selectedList.Add(new SelectListItem
                {
                    Value = organisation.OrganisationId.ToString(),
                    Text = organisation.Name
                });
            }

            return selectedList;
        }
    }
}