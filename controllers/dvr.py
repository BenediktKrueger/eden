# -*- coding: utf-8 -*-

module = request.controller
resourcename = request.function

if not settings.has_module(module):
    raise HTTP(404, body="Module disabled: %s" % module)

# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    #return s3db.cms_index(module, alt_function="index_alt")
    return {}

# -----------------------------------------------------------------------------
def index_alt():
    """
        Module homepage for non-Admin users when no CMS content found
    """

    # Just redirect to the list of Cases
    s3_redirect_default(URL(f="case"))

# -----------------------------------------------------------------------------
def person():
    """ Persons: RESTful CRUD Controller """

    # Set the default case status
    default_status = s3db.dvr_case_default_status()

    def prep(r):

        # Filter to persons who have a case registered
        resource = r.resource
        resource.add_filter(FS("dvr_case.id") != None)

        if r.component and r.id:
            ctable = r.component.table
            if "case_id" in ctable.fields and \
               str(ctable.case_id.type)[:18] == "reference dvr_case":

                case_id = ctable.case_id

                dvr_case = s3db.dvr_case
                query = (dvr_case.person_id == r.id) & \
                        (dvr_case.deleted != True)
                cases = db(query).select(dvr_case.id, limitby=(0, 2))

                if len(cases) == 1:
                    case_id.default = cases.first().id
                    case_id.readable = case_id.writable = False
                else:
                    case_id.requires = IS_ONE_OF(db(query), "dvr_case.id",
                                                 case_id.represent,
                                                 )

        if r.interactive:

            # Adapt CRUD strings to context
            s3.crud_strings["pr_person"] = Storage(
                label_create = T("Create Case"),
                title_display = T("Case Details"),
                title_list = T("Cases"),
                title_update = T("Edit Case Details"),
                label_list_button = T("List Cases"),
                label_delete_button = T("Delete Case"),
                msg_record_created = T("Case added"),
                msg_record_modified = T("Case details updated"),
                msg_record_deleted = T("Case deleted"),
                msg_list_empty = T("No Cases currently registered")
                )

            if not r.component:

                # Module-specific CRUD form
                from s3 import S3SQLCustomForm, S3SQLInlineComponent
                crud_form = S3SQLCustomForm(
                                "dvr_case.reference",
                                "dvr_case.organisation_id",
                                "dvr_case.date",
                                "dvr_case.status_id",
                                "first_name",
                                "middle_name",
                                "last_name",
                                "date_of_birth",
                                "gender",
                                S3SQLInlineComponent(
                                        "contact",
                                        fields = [("", "value"),
                                                  ],
                                        filterby = {"field": "contact_method",
                                                    "options": "EMAIL",
                                                    },
                                        label = T("Email"),
                                        multiple = False,
                                        name = "email",
                                        ),
                                S3SQLInlineComponent(
                                        "contact",
                                        fields = [("", "value"),
                                                  ],
                                        filterby = {"field": "contact_method",
                                                    "options": "SMS",
                                                    },
                                        label = T("Mobile Phone"),
                                        multiple = False,
                                        name = "phone",
                                        ),
                                "person_details.nationality",
                                S3SQLInlineComponent(
                                        "address",
                                        label = T("Current Address"),
                                        fields = [("", "location_id"),
                                                  ],
                                        filterby = {"field": "type",
                                                    "options": "1",
                                                    },
                                        link = False,
                                        multiple = False,
                                        ),
                                "dvr_case.comments",
                                )

                # Module-specific filter widgets
                from s3 import get_s3_filter_opts, S3TextFilter, S3OptionsFilter
                filter_widgets = [
                    S3TextFilter(["first_name",
                                  "middle_name",
                                  "last_name",
                                  #"email.value",
                                  #"phone.value",
                                  "dvr_case.reference",
                                  ],
                                  label = T("Search"),
                                  comment = T("You can search by name or case number"),
                                  ),
                    S3OptionsFilter("dvr_case.status_id",
                                    cols = 3,
                                    default = default_status,
                                    #label = T("Case Status"),
                                    options = s3db.dvr_case_status_filter_opts,
                                    sort = False,
                                    ),
                    S3OptionsFilter("person_details.nationality",
                                    ),
                    ]

                resource.configure(crud_form = crud_form,
                                   filter_widgets = filter_widgets,
                                   )

        # Module-specific list fields (must be outside of r.interactive)
        list_fields = ["dvr_case.reference",
                       "first_name",
                       "middle_name",
                       "last_name",
                       "date_of_birth",
                       "gender",
                       "dvr_case.date",
                       "dvr_case.status_id",
                       ]
        resource.configure(list_fields = list_fields,
                           )

        return True
    s3.prep = prep

    return s3_rest_controller("pr", "person", rheader = s3db.dvr_rheader)

# -----------------------------------------------------------------------------
def case_activity():

    def prep(r):

        resource = r.resource
        list_fields = ["case_id$reference",
                       "person_id$first_name",
                       "person_id$last_name",
                       "need_id",
                       "need_details",
                       "emergency",
                       "referral_details",
                       "followup",
                       "followup_date",
                       "completed",
                       ]
        resource.configure(list_fields = list_fields,
                           insertable = False,
                           deletable = False,
                           )
        return True
    s3.prep = prep

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def case_status():
    """ Case Statuses: RESTful CRUD Controller """

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def case_type():
    """ Case Types: RESTful CRUD Controller """

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def case():
    """ Cases: RESTful CRUD Controller """

    s3db.dvr_case_default_status()

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def need():
    """ Needs: RESTful CRUD Controller """

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def housing():
    """ Housing: RESTful CRUD Controller for option lookups """

    s3.prep = lambda r: r.method == "options" and \
                        r.representation == "s3json"

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def housing_type():
    """ Housing Types: RESTful CRUD Controller """

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def beneficiary_data():
    """ Beneficiary Data: RESTful CRUD Controller """

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def beneficiary_type():
    """ Beneficiary Types: RESTful CRUD Controller """

    return s3_rest_controller()

# END =========================================================================
