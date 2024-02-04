# tables

    ### Distinctiveness and Complexity

        * Implemented encoding and decoding function. (For all 149186 Unicode characters avalibility in 26 english letters and 0 digits characters) and AES cryptography function with internal security-key and minimul string lenght.
        * Implementing "getter" and "setter" systems in database models get and save values for guarantee encoded data saved and decoded whats are get from DB.
        * Contains 10 applications.
        * Using postgreSQL database.
        * Contains commerce, messaging, todo list and ... units, Django backend and Javascript frontend.
        * Using memory maintenance management systems as "Lazy Loading", "Mamory Caching" or "Prefetching".
        * Common application within main 10 applications, contains "utils" package for common functions and classes which I have wroted.
        * Creating multi level models are seprated in modules there in sub packages.
        * Developing admin dashboard for multy applications system.
        * Deep UI locally using Swiper and Bootstrap.
        * Set user groups and access rights, using django AbstractUser, Group, Permission classes.
          * Access menus permision management.
        * Creating custom Django tamplate filters and tag.
        * In this project, we have employed JSON Web Tokens (JWT) through Django's rest_framework_simplejwt to secure our user authentication system. This allows us to provide token-based authentication, ensuring the integrity and confidentiality of user data. We've tailored the token lifetimes to be adjustable per user or user group, offering a more granular control over session expirations. Additionally, meticulous strategies have been developed to manage expired and blacklisted tokens, keeping the authentication ecosystem clean and efficient. Through these mechanisms, we've built a secure, user-friendly authentication architecture, showcasing a distinctive and complex approach to ensuring user data security in our application.
        * Utilizing context_processo: In this project, given the use of JWT tokens, we realized that Django's traditional method for providing user context in templates lacked the necessary efficiency. Therefore, we created a custom context_processor to make the current user's information accessible in all templates using the token. This capability enables us to effortlessly display user information across various pages of the application without having to send user information to each view separately.
        * Creating Custom Decorators: Furthermore, we have crafted custom decorators to better manage access permissions. These decorators allow for the examination and enforcement of access permissions based on the specific needs of the application. Through this approach, we have ensured that only authorized users can access different resources within the application.
        * the Django Debug Toolbar was utilized to ensure efficient debugging and performance optimization. This tool is instrumental in providing real-time feedback on the performance of our Django application. To activate the Debug Toolbar, it was necessary to install it via pip (pip install django-debug-toolbar), and subsequently add 'debug_toolbar' to the INSTALLED_APPS section, and 'debug_toolbar.middleware.DebugToolbarMiddleware' to the MIDDLEWARE section of our Django settings. Moreover, the internal IPs were configured to recognize our local setup. The Debug Toolbar is visible only when DEBUG is set to True, ensuring it's deactivated in a production environment, maintaining the security and efficiency of our application. This setup significantly aided in identifying and resolving performance bottlenecks, thereby streamlining the development process.
        * HTTPS Implementation:
          * To enhance security, HTTPS was enabled in the project by obtaining and installing an SSL certificate, configuring Django settings, and modifying the application's URL for secure communication.
        * CORS and Allowed IPs:
          * CORS functionality was added using the django-cors-headers package, and specific IP addresses were authorized in the Django settings to access project resources. 
        * Setting up Redis Server:
          * In the course of the project, we successfully set up a Redis server to enhance the efficiency of data storage and retrieval operations. This enables faster data access, which is crucial for the real-time performance needs of the application.
        * JavaScript Compilation with Babel and Webpack.
        * Modal Component in React for Table Interaction and JavaScript and HTML-Bootstrap modal implementation: his section of the codebase showcases advanced functionalities, leveraging diverse tools like jQuery for DOM manipulation and React Table library for robust table rendering. The usage of these technologies empowers interactive features within the code, providing a seamless user experience and enhancing the overall functionality.

    ### Files content

        1- common/utils/
          * crypto, (common/utils/crypto.py): encryption functions and decryption ones.
          * Dynamic code change (common/utils/codehelp.py): Functions are dinamically changes group of modules programatcally using Regular Exprssion.
        2- node_modules directory: contains swiper css and js files and React framework files locally.
        3- GeoLite2-City.mmdb defined in settings.py (GEOIP_PATH = 'path') is MaxMind GeoLite2 City database.
        4- node_modules:
            * bootstrap
            * jquer
            * js-tokens
            * intl-tel-input
            * swiper
            * scheduler
            * react
            * react-dom
            * loose-envify

    ### Running

        * Install Dependencies: Navigate to the project directory and run npm install to install all necessary dependencies specified in package.json.
        * (Not activated for default. It's an optional item is not defined using in appropriated templates) Compile JavaScript Code: Use the command npm run build to trigger Webpack for compiling the JavaScript files. This will generate an ES5-compatible bundle.js file in the specified output directory.
        * Run redis-server
        * Run python manage.py runsslserver.
        

    #### Video Demo:  <URL HERE>

    #### Description

    ### Notes
        ## Preliminaries and generalities
            1- Semantic Versioning Implementation
            Implementing Semantic Versioning (SemVer) in my project signifies a commitment to clear and meaningful version numbers. In the heart of settings.py, the declaration VERSION = "0.1.0" marks the inception of my project with version 0.1.0. This not only sets a solid foundation but also establishes a convention for version increments, adhering to SemVer principles. As I progress, version updates will transparently communicate the nature of changes, ensuring compatibility and facilitating a streamlined development process.
            2- Have generating this project multilingual.
            3- Made React files locally using native "react.production.min.js" and "react-dom.production.min.js" files. ("npm install react react-dom" command)
            4- Create Swiper pictures with: "https://unpkg.com/swiper/swiper-bundle.min.js" and "https://unpkg.com/swiper/swiper-bundle.min.css" thate have made locally.
            5- Localize Bootstrap in node_modules directory which is in project's root
            6- The data exchange system encompasses various HTTP protocols within the server-side API implementation. The SettingsGetTableContentView APIView facilitates data retrieval via the GET protocol. The ModifyModelViewSet in the server-side implements multiple protocols:
            POST protocol: Sending model instances to the server by overriding the create method.
            PUT protocol: Implementing complete model field updates through the update method override.
            PATCH protocol: Changing specific fields of a model instance by overriding the partial_update method.
            DELETE protocol: Deletion of a model instance with soft deletion via setting the deleted_at field using date and time information, inherited across all models.
            Moreover, robust data validation procedures are incorporated pre-transmission, ensuring data accuracy. The system delivers appropriate messages and tooltips to guide users effectively, enhancing user experience and aiding in error prevention.
    1. settings.py managed:
        * 11 applications definition:
            * administration
            * common
            * financialhub
            * nursing
            * treatment
        * Database defined as postgresql
        * Caching models function in memory.
        * Global static folder defined which is in projects root.
        * Using <picture> and <source> tag for images responsivety within mobile devices and desktop ones.
        * Lazy image loading for priority loading page DOM contents first.
        * Database Addressing using DATABASE_URL:
            For a more concise and unified method of database connection, the database was addressed using DATABASE_URL in the settings.py. This method streamlines the process of database connectivity and ensures easier configuration in diverse environments.
        * Implementing environ for Environment Variables:
            To ensure the security and modularity of the project, we incorporated the use of environ to manage environment variables. This allows sensitive data such as secret keys and database credentials to be stored outside the codebase, thus enhancing the security posture of the application.
    2. Models
        0- Models detail:
            . Customise models setting using Meta sub class, save method.
            . Upload Image on server.
            . Using database signal functions for delete files from server according to db deletion.
            . customizing save method of models.
            . Have initial models data validation and sorting records.
            . Fields validation using fields validators parameter or clean method and call validator function.
            . Using self relation models such as in menus and sub-menus creation.
            . Audit Log center using signal models actions.
        1- Create base classes in the "common" application.
            . Creating an abstract model for inheritance its common fields in all another models.
            . Make auto_now editable false.
            . Using TextField data type in django models for long lenght encoded data will entry, sith setting "admin.widgets.AdminTextareaWidget(attrs={'rows': 1})" class in admin.py for change TextField view in model profile data entry to text box and using Media class to use css settings for it be same the CharField.
            . Using @property and setter and getter with save method for auto encoder, decoder data entry or export in database.
            . Using TextField datatype for encoded fields because has large encoded data with css for admin profile whitch uses to textbox fields in add.
            . Creating Translate model for translate phrase or each units of language to another language.
            . Creating SettingMenus which has Self-referential ForeignKey, modeing menu and submenu items.
            . Using PhoneNumberField from phonenumber_field.modelfields package for models phone numbers validation check.
        2- Developing treatment application models in not regular structure!
            . Using  abstract inheritance from common's model modules and ForeignKey relation to them.
            . Create packeage for medels, contains separated model files are inside.
            . Create specialist package in models package and madules contain related models under.
        3- Developing accommodation models.py
        4- Developing administration models.py
        5- Developing communication models.py
        6- Developing financialhub models.py
        7- Developing food models.py
        8- Developing nursing models.py
        9- Developing shopping models.py
        10- Developing tourism models.py
        11- Developing transportation models.py
        12- Initialy some recorrds are added to tables, using models structure.
    3. Templates
       1. common application.
            . localizing Bootstrap and React and swiper css and js and ... files.
            . generating swiper pictures with lazy loading.
            . Using multilevel dropdown menus.
            . Include Django template codes in central template.
            . Creating {% calculate %} custom tag for Django templates which has (+, -, *, /) operator on numbers as globaly variable have access them in ever templates. [StackOverflow](https://stackoverflow.com/a/77160358/17473587)
            . Detailing the HTML implementation of modals using Bootstrap, this section delves into the creation and usage of modals within the HTML structure. It emphasizes Bootstrap's role in facilitating the creation of modals and sheds light on the technical aspects of employing HTML elements in conjunction with Bootstrap for modal functionality.
    4. Control
       1. Sessions: start using cookies session.
       2. Creating custome user permision decorators.
       3. Creating custome context processors for Django template user context. 
       4. Using CBV(Class-Based Views) across FBV(Function-Based Views).
       5. Using (DRF)Django REST framework and JWT(JSON Web Token) for end-users and APIs system security and athentication. (Classic Django security system is unused abandoned)
       6. Using GeoIP2 for catch users region from his ip.
       7. Implemented functions to extract client's IP and system proxy settings for subsequent use such as location determination and country code retrieval. The get_client_ip function derives the client's IP from the request meta, while get_system_proxy function fetches system's proxy settings from the environment variables.
       8. a custom middleware, JWTAuthenticationMiddleware, was implemented to enhance the authentication process within a Django REST framework. This middleware extracts the JWT token from cookies upon receiving a request, populates request.user with the user information decoded from the JWT, and also sets the Authorization header with the token for DRF's built-in authentication classes to function correctly, ensuring a seamless integration of authentication mechanisms in a secure manner.
       9. Security:
          1.  In this project, I successfully implemented a robust system for refreshing access tokens using refresh tokens. Leveraging Django Rest Framework and a custom APIView, I extended the TokenRefreshView to seamlessly renew access tokens. The implementation addressed potential challenges through meticulous error handling and security measures, resulting in an enhanced authentication process. The integration of JWT and refresh tokens significantly improved the project's security and overall efficiency, providing a solid foundation for future optimizations.
    5. User Side (javascript)
       1. Using async/await across fetch.
       2. In the login template, the JavaScript code utilizes the Geolocation API to retrieve the user's GPS coordinates upon permission. It dynamically creates hidden input fields, populating them with the latitude and longitude, and appends these to the login form, ensuring the GPS data is sent along upon submission. In case of an error, it logs the issue to the console. 
       3. Utilized Django alongside JavaScript to implement a system for fetching the country code based on the user's IP. Integrated the intl-tel-input library to automatically populate the country code field, enhancing user experience during the phone number input process. 
       4. Dynamic Table Creation:
        This project uses JavaScript to dynamically create tables based on serialized data from the server. The process involves requesting data, receiving the serialized data response, and then dynamically generating a table to represent this data. This ensures the table is always up-to-date with the underlying data.
       5. Client-Side Pagination Tool:
          This JavaScript tool provides a comprehensive solution for client-side pagination. It's designed with a focus on modularity and user interaction. The tool dynamically generates pagination elements, manages their positioning, and handles user navigation events. It also intelligently adapts the URL based on the current page. Styled with Bootstrap but entirely implemented in JavaScript, this tool offers a seamless user experience for navigating through pages in your project.
       6. Tooltip Component: 
       Our Tooltip Component leverages JavaScript and Bootstrap functionalities to display concise messages and provide useful information to users within our project. This component offers a user-friendly way to present necessary information with flexibility in customization. We've utilized jQuery for handling user interactions and events. To ensure an appealing user interface, Bootstrap features have been employed to customize the tooltip appearance. Additionally, through JavaScript, we manage the display duration of the tooltip upon activation, automatically hiding it after a defined time interval. This component is easily integrable and extensible, seamlessly adaptable to various projects.

    6. User Side (React library)
       1. This segment delves into the intricacies of React's capabilities and technical insights embedded within the code. It highlights how React was employed to create interactive modals and manage the state of related tables, emphasizing the technical nuances and programming paradigms involved in achieving these functionalities.
       2. Tooltip Component: 
       The TooltipComponent is a React-based tool designed to effortlessly generate and display tooltips for specific elements within an application. Leveraging React's functionalities, it dynamically creates tooltips using the Overlay component from React Bootstrap. By customizing attributes like placement and appearance, it allows flexible and tailored tooltip presentations. This component's efficiency lies in its ability to seamlessly attach tooltips to designated elements, ensuring a smooth user experience by providing informative and context-sensitive hints or messages. Additionally, it prioritizes clean resource management by handling the removal of tooltips upon component unmounting.
       
    ### Technical Details
       1.  Throttling is implemented in this project to control the rate of requests. The global throttle setting is configured in the        settings.py file with a 'custom' scope set to '2/second'. This limit can be adjusted as necessary based on the API usage
       2.  Create local static in the project root, using STATICFILES_DIRS list which is in settings.py.
       3.  Localize GeoLite2-City.mmdb using with django.contrib.gis.geoip2 for extract geographical informations from longitude and latitude.
       4.  logging system
            Incorporated a logging system by configuring Django's LOGGING setting in settings.py, enabling the capture of server errors and warnings into a file named debug.log. This streamlined the debugging process, ensuring a smoother development workflow and easier issue tracking.
            The logging mechanism was improved to capture detailed application activities, aiding in debugging and providing transparency in application operations. This advancement ensures that any anomalies or issues can be traced effectively, ensuring smooth application operations. 
            An advanced logging mechanism was implemented in the Django application using Python's logging and logging.handlers modules. A QueueHandler and RotatingFileHandlers were configured for different log levels (error, warning, and debug) to efficiently manage log files, ensuring thread-safety and reliable error tracing with a maximum log file size of 10MB, while QueueListeners were utilized to delegate log records to appropriate file handlers, aiding in effective debugging and monitoring.
       5.  Creation and Configuration of .env File
            To further the implementation of environment variables, a .env file was created. Recommended variables from the settings.py were externalized to this file. This modular approach ensures that configurations can be changed without altering the main codebase, promoting maintainability.
       6. Caching Policy
            In managing our project's caching strategy, I've drawn inspiration from the Harvard University CS50 course to ensure optimal performance. Leveraging Django signals, specifically post_save, I've implemented a mechanism triggering cache invalidation upon data modifications. The key player here is the delete_pattern method, tactically wiping out any cache entries matching the 'settings_serialized_model_*' pattern.            
            To further fortify our caching infrastructure, I've introduced a versioning system. This involves maintaining a VERSION variable in our settings.py file, ensuring that cache keys remain coherent even in the face of software upgrades.            
            Speaking of cache keys, they're crafted with precision. The key structure, exemplified by settings_serialized_model_{id}_{page}:{version}, guarantees not only efficiency but also accuracy in data retrieva            
            In essence, this approach mirrors industry best practices, promising a responsive and adaptable Django application that stays on top of data changes with finesse.
       7. Server-Side Pagination in Action, Serializer Implementation
            The server-side pagination functionality is showcased in the SettingsGetTableView view. This APIView employs the fetch_related_data function to retrieve related data, utilizing the standardized pagination to manage large datasets. The paginated results are then cached for an hour, ensuring swift access to frequently requested information.
            In the realm of serializing models within Django, a comprehensive and dynamic approach was undertaken. The serialize_model function was crafted to generate a customized model serializer dynamically. This enabled the adaptation of serialization to any Django model, fostering reusability and scalability.
            The ModelInfoSerializer and FieldInfoSerializer were meticulously developed to extract essential information about models and their fields. The former provides insights into the model name, app, and editability, while the latter delves into field-specific details such as name, type, and editability. This modular and versatile serializer structure ensures adaptability to various data structures.       
            Furthermore, the AggregateModelInfoSerializer consolidates model and field information into a cohesive representation. This serializer encapsulates the metadata of a Django model, including details about its fields. The resulting structure, enriched with both model and field information, forms a holistic view of the serialized model.
       8. Pagination Enhancement
            To augment data retrieval efficiency, a tailored pagination mechanism was integrated. The StandardResultsSetPagination class, a customized pagination solution, optimizes the presentation of large datasets by breaking them into manageable chunks. This paginator seamlessly integrates with the existing Django Rest Framework infrastructure, providing a smoother user experience and improving overall system performance.
       9. JavaScript Compilation with Babel and Webpack
           This project utilizes Babel and Webpack to compile JavaScript code from ES6 to ES5, ensuring compatibility across different browsers, including older versions. Babel is configured with the @babel/preset-env to transpile modern JavaScript syntax, while Webpack is set up with module rules specifying Babel-loader exclusion of node_modules. The compilation command npm run build triggers Webpack to bundle the JavaScript files, generating an ES5-compatible bundle.js file. This setup allows for the utilization of modern JavaScript features while maintaining support for older browsers, enhancing code efficiency and cross-browser compatibility in the project.
        10. Permissions security control:
                - Each menu item is associated with a field in the SettingMenus instance called 'individual_permission'.
                - This field has a many-to-many relationship with manually defined instances of the built-in auth.Permission model.
                - This relationship is used to define access permissions for each menu item.
                - Access permissions are checked using a custom Django template tag called 'has_permission', which is located in the common.permissions.py module.
                - Additionally, the manipulation of models in the dynamic table application is handled with view CRUD permission checking.
                - This is done using the DRF CustomModelPermission class, also located in the common.permissions.py module.
                - This class grants user access to those who are authorized."
