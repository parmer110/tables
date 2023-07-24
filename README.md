# Floramedtour

    ### Distinctiveness and Complexity

        * Implemented encoding and decoding function. (For all 149186 Unicode characters avalibility in 26 english letters and 0 digits characters) and AES cryptography function with internal security-key and minimul string lenght.
        * Implementing "getter" and "setter" systems in database models get and save values for guarantee encoded data saved and decoded whats are get from DB.
        * Contains 8 applications.
        * Using postgreSQL database.
        * Contains commerce, messaging, todo list and ... units, Django backend and Javascript frontend.
        * Using memory maintenance management systems as "Lazy Loading", "Mamory Caching" or "Prefetching".
        * Common application within main 7 applications, contains "utils" package for common functions and classes which I have wroted.

    ### Files content

        * crypto, (common/utils/crypto.py): encryption functions and decryption ones.

    ### Running

        * python manage.py runserver.

    #### Video Demo:  <URL HERE>

    #### Description

    1. settings.py managed:
        * 6 applications definition:
            * food
            * nursing
            * shopping
            * stay
            * tourism
            * transportation
            * treatment
        * Database defined as postgresql
        * Caching models function in memory.
    2.

    ### Notes

    1- Create base classes in the "common" application.
        . Using TextField data type in django models for long lenght encoded data will entry, sith setting "admin.widgets.AdminTextareaWidget(attrs={'rows': 1})" class in admin.py for change TextField view in model profile data entry to text box and using Media class to use css settings for it be same the CharField.
    2- 
