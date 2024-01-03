// Table introduction

document.addEventListener('DOMContentLoaded', function() {
    // Load contexts
    for (var i = 0; i < applicationNames.length; i++) {
        const applicationName = applicationNames[i];
        let tableName = tableNames[i];
        
        console.log("Application Name:", applicationName);
        console.log("Table Name:", tableName)
    }        
});