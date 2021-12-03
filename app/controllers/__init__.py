def init_controllers(app):
    import app.controllers.api.account.route
    import app.controllers.api.staff.route
    import app.controllers.api.department.route
    import app.controllers.api.position.route
    import app.controllers.api.document.route
    import app.controllers.api.upload.route
    import app.controllers.api.unit.route
    import app.controllers.api.document_type.route
    import app.controllers.api.document_expires.route
    import app.controllers.api.document_admin.route
    import app.controllers.api.document_manager.route
    import app.controllers.api.document_staff.route
    import app.controllers.api.document_report.route
    import app.controllers.api.statistic.route
    import app.controllers.api.permission.route
    import app.controllers.api.user_role.route