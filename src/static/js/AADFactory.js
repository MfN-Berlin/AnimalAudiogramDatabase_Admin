/**Creates the controllers for experiment, animal and data points*/
class AADFactory {
    
    createAnimalController() {
        var dao = new AnimalDAO();
        var view = new AnimalJsonFormatter(dao)
        var controller = new AnimalController(view, dao);
        return controller;
    }
    
    createTaxonomyController() {
        var dao = new TaxonomyDAO();
        var view = new TaxonomyJsonFormatter(dao)
        var controller = new TaxonomyController(view, dao);
        return controller;
    }
    
    createDataPointController() {
        var dao = new DataPointDAO()
        var view = new DataPointJsonFormatter(dao);
        var controller = new DataPointController(view, dao);
        return controller;
    }
    
    createExperimentController() {
        var dao = new ExperimentDAO();
        var view = new ExperimentJsonFormatter(dao);
        var controller = new ExperimentController(view, dao);
        return controller;
    }
    
    createPublicationController() {
        var dao = new PublicationDAO();
        var view = new PublicationJsonFormatter(dao);
        var controller = new PublicationController(view, dao);
        return controller;
    }
}
