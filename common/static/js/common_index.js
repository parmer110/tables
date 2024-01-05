'use strict';

// References
import { createElement, StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { TModal, DynamicTableComponent } from './components.js';
import { FaTrashAlt } from 'react-icons/fa';


// Global Variables declaration
const SESSION_TAG_KEY = "tag";
const SESSION_PAGE_KEY = "page";
const SESSION_ID_KEY = "item";
const awEdit = `<i class="fas fa-edit clickable" style="color: blue;"></i>`;
const awTrash = `<i class="fas fa-trash-alt clickable" style="color: red;"></i>`;
const awCheck = `<i class="fas fa-check clickable" style="color: green;"></i>`;
const awCross = `<i class="fas fa-times clickable" style="color: red;"></i>`;
// localStorage.clear();
let isUserAuthenticated = false;
let savedTag;
let savedPage;
let savedId;

// Common functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function refreshToken() {
    
    var intervalId;
    var timeoutID;

    fetch('token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            clearInterval(Number(sessionStorage.getItem('intervalId')));
            clearTimeout(Number(sessionStorage.getItem('timeoutID')));
                throw new Error(`Error: ${response.status}`);
        }
        isUserAuthenticated = true;
        return response.json();
    })
    .then(data => {
        clearInterval(Number(sessionStorage.getItem('intervalId')));
        clearTimeout(Number(sessionStorage.getItem('timeoutID')));

        var access_token_expiry = getCookie('access_token_expiry');

        timeoutID = setTimeout(function() {
            // This will start running every 2 seconds after the delay
            isUserAuthenticated = false;
            intervalId = setInterval(refreshToken, 5 * 1000);
            sessionStorage.setItem('intervalId', intervalId);
        }, Number(access_token_expiry) * 1000 - 2 * 60 * 1000);
        sessionStorage.setItem('timeoutID', timeoutID);

        let currentTime = new Date();
        console.log(currentTime.toLocaleTimeString());

    })
    .catch(error => {
        clearInterval(Number(sessionStorage.getItem('intervalId')));
        clearTimeout(Number(sessionStorage.getItem('timeoutID')));

        console.error(`Error in token refresh: ${error.message}`);
        // window.location.href = "/login/";
    });
}

// Session (send)
async function sendToServer(method, path, body, qs="") {
    // const csrf_token = document.cookie.match(/csrftoken=([^;]+)/)[1];
    const url = `${path}${qs ? '?' + qs : ''}`;
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return fetch(url, {
        method: `${method}`,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Authorization': `eslope`
        },
        body: JSON.stringify(body)
    })
    .then(response => {
        if (response.ok && response.status === 204) { // No Content
            return {status: response.status};
        } else {
            return response.json().then(data => ({...data, status: response.status}));
        }
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Session (get)
async function getFromServer(path, qs="") {
    try {
        const url = `${path}${qs ? '?' + qs : ''}`;
        const response = await fetch(url, {
            headers: {
                'Authorization': `eslope`
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error; 
    }
}


function convertToString(value) {
    return (value === null || value === undefined || value === "") ? "" : value.toString();
}

function convertToValidData(dataString, dataType) {
    
    function stringToInt(stringData) {
        return parseInt(stringData, 10);
    }

    function stringToFloat(stringData) {
        return parseFloat(stringData);
    }

    function stringToBoolean(stringData) {
        let boolValue;
        try {
            boolValue = JSON.parse(stringData);
        } catch {
            boolValue = "";
        }
        return boolValue;
    }

    function stringDateTime(stringData) {
        let date = new Date(stringData);
        if (isNaN(date.getTime())) {
            console.error(`Date time: ${date} is invalid!`);
        } else {
            return date;
        }
    }

    const converters = {
        'int': stringToInt,
        'float': stringToFloat,
        'boolean': stringToBoolean,
        'datetime': stringDateTime
    };
    
    if (!dataString) {return null;}
    for (let key in converters) {
        if (dataType.toLowerCase().includes(key)) {
            return converters[key](dataString);
        }
    }

    return dataString;
}

function convertStringToIntegerArray(numberString) {
    if (!/\d/.test(numberString)) {
        return [];
    }
    
    const numberArray = numberString.split(/[,\s]+/);
    const integerArray = numberArray.map(number => parseInt(number, 10));
    return integerArray;
}

function getMenuTrail(tag) {
    let text = tag.innerText;
    while (tag.parentElement && tag.parentElement.parentElement && tag.parentElement.parentElement.previousElementSibling) {
        tag = tag.parentElement.parentElement.previousElementSibling;
        text = `${tag.innerText} ${text}`;
    }

    text = text.replace(tag.innerText, `${tag.innerText} »`);
    return text;
}

function showWarningTooltip(element, text, timeOut=5) {
    const tooltip = $('<div class="custom-tooltip"></div>');
    tooltip.text(text);
    
    const targetElement = $(element);
  
    $('body').append(tooltip);
  
    const tooltipWidth = tooltip.outerWidth();
    const targetOffset = targetElement.offset();
    let targetOffsetLeft, top;
    if (targetOffset) {
        targetOffsetLeft = targetOffset.left;
        top = targetOffset.top;
    } else {
        top = 0;
        console.error('Element offset is undefined');
    }
    const targetWidth = targetElement.outerWidth();
    const windowWidth = $(window).width();
  
    let leftPos = targetOffsetLeft + (targetWidth / 2) - (tooltipWidth / 2);
  
    // Check if the tooltip exceeds the right edge of the window
    if (leftPos + tooltipWidth > windowWidth) {
      leftPos = windowWidth - tooltipWidth;
    }
  
    // Check if the tooltip exceeds the left edge of the window
    if (leftPos < 0) {
      leftPos = 0;
    }
  
    tooltip.css({
      top: top - tooltip.outerHeight() - 10,
      left: leftPos
    }).fadeIn();

    var timeoutId = setTimeout(function() {
        tooltip.fadeOut(function() {
            $(this).remove();
        });
    }, timeOut * 1000);
  
    $(document).on('click', function(e) {
      if (!$(e.target).closest('.custom-tooltip').length && !$(e.target).is(element)) {
        tooltip.fadeOut(function() {
          $(this).remove();
        });
      }
    });
}

function showAlertTooltip(element, text, timeOut=5) {
    const tooltip = $('<div class="custom-tooltip"></div>');
    const targetElement = $(element);
  
    // Check if the text is an object (such as errorObj) and convert it to a user-friendly format
    if (typeof text === 'object' && text.errorCount !== undefined && text.validationReport !== undefined) {
      const formattedErrorText = formatErrorObject(text);
      tooltip.html(formattedErrorText);
    } else {
      tooltip.text(text);
    }
  
    $('body').append(tooltip);
  
    const tooltipWidth = tooltip.outerWidth();
    const targetOffset = targetElement.offset();
    let targetOffsetLeft, top;
    if (targetOffset) {
        targetOffsetLeft = targetOffset.left;
        top = targetOffset.top;
    } else {
        top = 0;
        console.error('Element offset is undefined');
    }
    const targetWidth = targetElement.outerWidth();
    const windowWidth = $(window).width();
  
    let leftPos = targetOffsetLeft + (targetWidth / 2) - (tooltipWidth / 2);
  
    // Check if the tooltip exceeds the right edge of the window
    if (leftPos + tooltipWidth > windowWidth) {
      leftPos = windowWidth - tooltipWidth;
    }
  
    // Check if the tooltip exceeds the left edge of the window
    if (leftPos < 0) {
      leftPos = 0;
    }
  
    tooltip.css({
      top: top - tooltip.outerHeight() - 10,
      left: leftPos,
      // Styling for a more modern and user-friendly tooltip appearance
      backgroundColor: '#333',
      color: '#fff',
      padding: '8px',
      borderRadius: '4px',
      boxShadow: '0 2px 5px rgba(0,0,0,0.3)',
      maxWidth: '300px', // You can adjust this to fit your design
    }).fadeIn();

    var timeoutId = setTimeout(function() {
        tooltip.fadeOut(function() {
            $(this).remove();
        });
    }, timeOut * 1000);
  
    $(document).on('click', function(e) {
      if (!$(e.target).closest('.custom-tooltip').length && !$(e.target).is(element)) {
        tooltip.fadeOut(function() {
          $(this).remove();
        });
      }
    });
  }
  
  // Function to format error object to a user-friendly text
function formatErrorObject(errorObj) {
    let formattedText = `<div class="tooltip-error-count">Error Count: ${errorObj.errorCount}</div>`;
    formattedText += '<hr>'; // Horizontal line for separation

    formattedText += '<div class="tooltip-validation-report">Validation Errors:</div>';
    formattedText += '<ul>';

    let fieldIndex = 1; // Start the index from 1

    errorObj.validationReport.forEach((error) => {
        // Check if the error text contains "Validation Errors:"
        if (!error.includes('Validation Errors:')) {
            formattedText += `<li>Error at (${fieldIndex}) field: ${error}</li>`;
            fieldIndex++; // Increment the index for each field
        }
    });

    formattedText += '</ul>';

    return formattedText;
}
  
function showConfirmationModal(message, title, buttonInfo) {
    return new Promise((resolve, reject) => {
        // ایجاد المان‌های مدال
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'confirmationModal';
        modal.tabIndex = '-1';
        modal.role = 'dialog';
        modal.setAttribute('aria-labelledby', 'exampleModalLabel');
        modal.setAttribute('aria-hidden', 'true');

        const modalDialog = document.createElement('div');
        modalDialog.className = 'modal-dialog';
        modalDialog.role = 'document';

        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';

        const modalHeader = document.createElement('div');
        modalHeader.className = 'modal-header';

        const modalTitle = document.createElement('h5');
        modalTitle.className = 'modal-title';
        modalTitle.innerText = title || 'Confirmation';
        modalHeader.appendChild(modalTitle);
        
        const closeButton = document.createElement('button');
        closeButton.type = 'button';
        closeButton.className = 'close';
        closeButton.setAttribute('data-dismiss', 'modal');
        closeButton.setAttribute('aria-label', 'Close');
        closeButton.innerHTML = '<span aria-hidden="true">&times;</span>';
        modalHeader.appendChild(closeButton);

        const modalBody = document.createElement('div');
        modalBody.className = 'modal-body';
        modalBody.innerHTML = message || 'Are you sure?';

        const modalFooter = document.createElement('div');
        modalFooter.className = 'modal-footer';

        const cancelButton = document.createElement('button');
        cancelButton.type = 'button';
        cancelButton.className = 'btn btn-secondary';
        cancelButton.setAttribute('data-dismiss', 'modal');
        cancelButton.innerText = buttonInfo['cancelButton'].text;
        modalFooter.appendChild(cancelButton);
        cancelButton.onclick = buttonInfo['cancelButton'].clickFunction;

        const confirmButton = document.createElement('button');
        confirmButton.type = 'button';
        confirmButton.className = 'btn btn-danger';
        confirmButton.innerText = buttonInfo['confirmButton'].text;
        modalFooter.appendChild(confirmButton);
        confirmButton.onclick = function() {
            this.disabled = true;
            buttonInfo['confirmButton'].clickFunction();
        }

        modalContent.appendChild(modalHeader);
        modalContent.appendChild(modalBody);
        modalContent.appendChild(modalFooter);

        modalDialog.appendChild(modalContent);
        modal.appendChild(modalDialog);

        document.body.appendChild(modal);

        // Running modal
        $('#confirmationModal').modal('show');

        closeButton.addEventListener('click', () => {
            $('#confirmationModal').modal('hide');
        });

        $('#confirmationModal').off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
            $(this).remove();
            delete window.confirmationModal;
            resolve('Modal closed');
        });
    });
}

// Modal dialog for related table
const relationModal = (parentMetadata, metadata, bodyRow, td) => {

    // Return choices from related table react.
    const createHandleReceiveSelectedIds = (parentMetadata, td) => {

        return (selectedId) => {

            let keyName = `editingTable_${parentMetadata['app']}_${parentMetadata['name']}`;
            keyName = keyName.toLowerCase();

            if (selectedId !== null && td.firstChild.value !== selectedId) {

                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control';
                input.readOnly = true;
                input.value = selectedId;
                td.innerHTML = "";
                td.appendChild(input);

                if (td.initRelateValue == selectedId) {
                    td.hasChanged = false;   
                    if (td.firstChild.classList.contains('is-valid')) {
                        td.firstChild.classList.remove('is-valid');
                    }                 
                } else {
                    td.hasChanged = true;
                    if (!td.firstChild.classList.contains('is-valid')) {
                        td.firstChild.classList.add('is-valid');
                    }                 
                }

                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {

                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }

                    sessionStorage.setItem(keyName, true);

                } else {
                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }    
                    sessionStorage.removeItem(keyName);
                }

                return selectedId;
            }
        };
    };
    const handleReceiveSelectedIds = createHandleReceiveSelectedIds(parentMetadata, td);

    // Modal table value initializer
    let initVal;
    if (td.firstChild.textContent) {
        initVal = td.firstChild.textContent;
    } else {
        initVal = td.firstChild.value;
    }
    
    // Modal
    const app = metadata['relatedApp'];
    const model = metadata['relatedModel'];
    let container = document.createElement('div');
    let firstChild = td.parentNode.firstChild.firstChild;

    let innerHTML = firstChild.firstChild.outerHTML;
    let innerText = firstChild.innerText;
    let isEditable = innerHTML === awCheck || innerText === 'Send';

    document.body.appendChild(container);
    const modal = 
        <TModal 
            elm={<DynamicTableComponent 
                getTableContent={getTableContent} 
                app={app} 
                model={model}    
                many={metadata['relationType'] === 'many-to-many' ? true : false}
                values={!initVal ? [] :initVal.split(",").map(Number)}
                editable={isEditable}
                onSelectedIdsChange={handleReceiveSelectedIds}
                />}
            app={app} 
            model={model}
            editable={isEditable}
            onClose={() => {
        document.body.removeChild(container);
        container = null;
    }} />;
    const root = createRoot(container);
    root.render(
        <StrictMode>
            {modal}
        </StrictMode>
    );
}

// Control buttons management
const controlRow = (table, record, bodyRow, td) => {

    let message;
    let tag;
    let keyName = `editingTable_${table['model_info']['app']}_${table['model_info']['name']}`;
    keyName = keyName.toLowerCase();
    const editableFieldsCount = table['field_info'].filter(obj => obj.editable === true && obj.type !== 'AutoField').length;
    const updFields = {};
    const updInvalid = {};
    const icon1 = document.createElement('i');
    const icon2 = document.createElement('i');
    const lineBreak = document.createElement('br');

    icon1.classList.add('icon1');
    icon1.classList.add('icon2');

    td.innerHTML = "";

    td.appendChild(icon1);
    td.appendChild(lineBreak);
    td.appendChild(icon2);

    icon1.innerHTML = awEdit;
    icon2.innerHTML = awTrash;

    // Edit Row
    icon1.addEventListener('click', async function() {
        if (!bodyRow.classList.contains('table-active') && !bodyRow.classList.contains('table-warning') && this.innerHTML == awEdit) {

            icon1.innerHTML = awCheck;
            icon2.innerHTML = awCross;

            bodyRow.className = 'table-active'; // Editing row indicator
            Array.from(bodyRow.children).forEach((cell, index) => {
                if (index !== 0) { // Skip the first cell
                    createEditingField(table, table['field_info'][index - 1], bodyRow, cell, keyName)
                }
            });
        } else if (bodyRow.classList.contains('table-active') && !bodyRow.classList.contains('table-warning') && this.innerHTML == awCheck) {
            exitEdition(bodyRow);
        } else if (!bodyRow.classList.contains('table-active') && bodyRow.classList.contains('table-warning') && this.innerHTML == awCheck) {
            // Confirm sending partial data to server
            const modalButtons = {
                'cancelButton': { text: 'Cancel',
                    clickFunction: () => {
                    $('#confirmationModal').modal('hide');
                } },
                'confirmButton': { text: 'Confirm', clickFunction: async() => {
                    Array.from(bodyRow.children).forEach((cell, index) => {
                        if (index !== 0) { // Skip the first cell
                            let fieldName = table['field_info'][index - 1]['name'];
                            let isEditableField = table['field_info'][index - 1]['editable'] && 
                                (table['field_info'][index - 1]['type'] !== 'AutoField');
                            let isNullable = table['field_info'][index - 1]['nullable'];
                            let fieldDataType = table['field_info'][index - 1]['type'];

                            if (isEditableField) {
                                if (cell.hasChanged) {
                                    if (cell.firstChild) {

                                        if (fieldDataType === 'ManyToManyField') {
                                            if(isNullable || cell.firstChild.value) {
                                                updFields[fieldName] = convertStringToIntegerArray(cell.firstChild.value);
                                            } else {
                                                updInvalid[fieldName] = cell.firstChild.value;
                                            }
                                        } else if(fieldDataType === 'ForeignKey' || fieldDataType === 'OneToOneField') {
                                            if (isNullable || cell.firstChild.value) {
                                                updFields[fieldName] = convertToValidData(cell.firstChild.value, 'integer');
                                            } else {
                                                updInvalid[fieldName] = cell.firstChild.value;
                                            }
                                        } else {
                                            if (cell.firstChild.checkValidity()) {
                                                updFields[fieldName] = convertToValidData(cell.firstChild.value, fieldDataType);
                                            } else {
                                                updInvalid[fieldName] = cell.firstChild.value;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    });
                    // Finalize sending rowData to the server
                    let application = table['model_info']['app'];
                    let model = table['model_info']['name'];
                    let body = {
                        application: application,
                        model: model,
                        data: updFields
                    }

                    if (Object.keys(updInvalid).length) {
                        message = 'Some incorrect data found!';
                        console.error(`This data are incorrect: ${updInvalid}`);
                        console.log(updInvalid);
                    } else {
                        if (Object.keys(updFields).length === editableFieldsCount) {
                            // Entire row updation
                            try {
                                let data = await sendToServer('PUT', `/table_update/${record.id}/`, body)

                                message = "Updated Instance!";
                                
                                Array.from(bodyRow.children).forEach((cell, index) => {
                                    if (index !== 0) {
                                        let key = table['field_info'][index - 1]['name'];
                                        if (key in data) {
                                            cell.hasChanged = false;
                                            cell.initRelateValue = data[key];

                                            const span = document.createElement('span');
                                            span.textContent = data[key];
                                            cell.innerHTML = '';
                                            cell.appendChild(span);

                                            bodyRow.className = "";
                                        }
                                    }
                                });

                                sessionStorage.removeItem(keyName); // Pagination handling permision

                                // Adding first cell control buttons
                                let icon1 = controlRow(table, data, bodyRow, bodyRow.firstChild)

                            } catch(error) {
                                // Data send to server Rejected or stablize handling issues.
                                message = "Unkown error in data handling! May server's issue";
                                console.error(`Error in new row handling. ${error}`);
                            };    

                        } else {
                            // Partial row updation
                            try {
                                let data = await sendToServer('PATCH', `/table_update/${record.id}/`, body)

                                if (data.ok) {
                                    message = 'Updated!';

                                    Array.from(bodyRow.children).forEach((cell, index) => {
                                        if (index !== 0) {
                                            let key = table['field_info'][index - 1]['name'];
                                            if (key in data) {
                                                cell.hasChanged = false;
                                                cell.initRelateValue = data[key];
    
                                                const span = document.createElement('span');
                                                span.textContent = data[key];
                                                cell.innerHTML = '';
                                                cell.appendChild(span);
    
                                                bodyRow.className = "";
                                            }
                                        }
                                    });

                                    sessionStorage.removeItem(keyName); // Pagination handling permision

                                    // Adding first cell control buttons
                                    let icon1 = controlRow(table, data, bodyRow, bodyRow.firstChild)
                                } else {
                                    console.log(data);
                                    message = await data.json();
                                }
                            } catch(error) {
                                // Data send to server Rejected or stablize handling issues.
                                message = ('Some incorrect data found!');
                                console.error(`Error in new row handling. ${error}`);
                            };
                        }    
                    }
                    
                    $('#confirmationModal').modal('hide');
                } }
            };
            await showConfirmationModal(`Are you sure you want to upload these changes to server?`, 'Confirmation!', modalButtons);
            if (message) {
                showAlertTooltip(bodyRow.firstChild, message);
            }
        }
    });

    const exitEdition = (bodyRow) => {
        icon1.innerHTML = awEdit;
        icon2.innerHTML = awTrash;
        if (!bodyRow.classList.contains('table-warning')) {
            bodyRow.classList.remove('table-warning');
        }
        if (bodyRow.classList.contains('table-active')) {
            bodyRow.classList.remove('table-active');
        }

        sessionStorage.removeItem(keyName);
        Array.from(bodyRow.children).forEach((cell, index) => {
            if (index !== 0) { // Skip the first cell
                if (table['field_info'][index - 1]['editable'] && table['field_info'][index - 1]['type'] !== 'AutoField') {
                    const span = document.createElement('span');

                    span.textContent = cell.firstChild.value;
                    cell.innerHTML = '';
                    cell.appendChild(span);
                }
            }
        });
    }

    // Delete row
    icon2.addEventListener('click', async function() {
        let delTag;
        let message;
        if (!bodyRow.classList.contains('table-active') && !bodyRow.classList.contains('table-warning') && this.innerHTML == awTrash) {
            
            $('#deleteModal').data('icon2', this);
            $('#deleteModal').modal('show');

            // Styling row Danger
            this.parentNode.parentNode.classList.add('table-danger');
            $('#deleteModal').on('hidden.bs.modal', function (e) {
                var icon2 = $(this).data('icon2');
                if (icon2) {
                    icon2.parentNode.parentNode.classList.remove('table-danger');
                }
            });

            // let defaultMsg = $('.modal-body').text();  // Store the default message
            let defaultMsg = $('.modal-body').html(); // Store the default message

            message = Array.from(bodyRow.querySelectorAll('td:not(:first-child)'))
            .map(td => td.textContent.trim())
            .filter(message => message !== '')
            .join('•••');

            // $('.modal-body').text(`Are you sure you want to delete this row?`);
            $('.modal-body').html(`<p>Are you sure you want to delete this row?</p><p>No undo performs!</p><p>${message}</p>`);

            $('#deleteButton').off('click').click(function() {
                var icon2 = $('#deleteModal').data('icon2');

                let body = {
                    application: table['model_info']['app'],
                    model: table['model_info']['name'],
                    id: record.id
                }
                sendToServer('DELETE', `/table_update/${record.id}/`, body)
                .then(data  => { // Data send to server Succeeded.
                    
                    if (bodyRow.nextElementSibling) {
                        tag = bodyRow.nextElementSibling.firstChild;
                    } else if (bodyRow.previousElementSibling) {
                        tag = bodyRow.previousElementSibling.firstChild;
                    } else {
                        tag = bodyRow.parentElement.previousElementSibling.firstChild.firstChild;
                    }

                    message = 'Row Deleted!';
                    bodyRow.remove();
                    
                    console.log('Deleted');
                    
                    if (message) {
                        showWarningTooltip(tag, message);
                    }
                })
                .catch(error => {
                    // Deleting model instance handling issues.
                    message = 'Server fault occurs!';
                    console.error(`Error in instance ommite. ${error}`);
                });    

                // // Reset the message to the default
                // $('.modal-body').text(defaultMsg);
                // Reset the message to the default
                $('.modal-body').html(defaultMsg);

                $('#deleteModal').modal('hide');
            });

        } else if (bodyRow.classList.contains('table-active') && !bodyRow.classList.contains('table-warning') && this.innerHTML == awCross) {
            exitEdition(bodyRow);
        } else if (!bodyRow.classList.contains('table-active') && bodyRow.classList.contains('table-warning') && this.innerHTML == awCross) {
            const modalButtons = {
                'cancelButton': { text: 'Cancel', clickFunction: () => {
                    $('#confirmationModal').modal('hide');
                } },
                'confirmButton': { text: 'Confirm', clickFunction: () => {
                    icon1.innerHTML = awEdit;
                    icon2.innerHTML = awTrash;
                    bodyRow.className = '';
                    message = "Row edition canceled!";
                    sessionStorage.removeItem(keyName);
                    if (record) {
                        Array.from(bodyRow.children).forEach((cell, index) => {
                            if (index !== 0) { // Skip the first cell
                                if (table['field_info'][index - 1]['editable'] && table['field_info'][index - 1]['type'] !== 'AutoField') {
                                    const span = document.createElement('span');
                                    span.textContent = record[table['field_info'][index - 1]['name']];
                                    cell.innerText = ""
                                    cell.appendChild(span);
                                    icon1.isEditing = false;
                                }
                            }
                        });                    
                    }
                    $('#confirmationModal').modal('hide');
                }}
            };
            await showConfirmationModal(`Are you sure you want to miss these changes?`, 'Warning!', modalButtons);
            if (message) {
                showWarningTooltip(bodyRow.firstChild, message);
            }
        }
    });
        // Event Listener HTML modal
        $('#crossButton, #cancelButton').off('click').click(function() {
            var icon2 = $('#deleteModal').data('icon2');
            // Can use icon2 to determine what action to take
            $('#deleteModal').modal('hide');
        });
    
    return icon1;
}

function createNewRow(table, tbody, addRowButton, keyName) {
    let message; 
    const newRow = document.createElement('tr');
    newRow.className = 'table-active'; // Editing row indicator
    tbody.prepend(newRow);

    // Create send button in the first cell of the new row
    const td = document.createElement('td');

    const sendButton = document.createElement('button');
    sendButton.classList.add('btn', 'btn-success');
    sendButton.innerText = 'Send';

    const icon = document.createElement('i');
    icon.innerHTML = awCross;

    td.appendChild(sendButton);
    td.appendChild(icon);
    newRow.appendChild(td);

    // Creating new row cells
    table['field_info'].forEach((field, index) => {
        const td = document.createElement('td');
        td.classList.add("max-width-cell");
        createEditingField(table, field, newRow, td, keyName);
        newRow.appendChild(td);
        if (field.name === 'created_at' || field.name === 'updated_at' || field.name === 'deleted_at') {
            td.classList.add('hidden');
        }
    });

    // Sending row data
    sendButton.addEventListener('click', async (event) =>{
        event.stopPropagation();
        message = '';
        let timeOut;
        if (newRow.classList.contains('table-warning')) {

            const modalButtons = {
                'cancelButton': { text: 'Cancel', clickFunction: () => {
                    $('#confirmationModal').modal('hide');
                }},
                'confirmButton': { text: 'Confirm', clickFunction: async () => {
        
                    const newRowData = {};

                    Array.from(newRow.children).forEach((cell, index) => {
                        if(index !== 0) {
                            
                            let fieldName = table['field_info'][index - 1]['name'];
                            let isEditableField = table['field_info'][index - 1]['editable'] &&
                                (table['field_info'][index - 1]['type'] !== 'AutoField');
                            let fieldDataType = table['field_info'][index - 1]['type'];
                            
                            if (isEditableField) {
                                if(cell.firstChild) {
                                    if (fieldDataType === 'ManyToManyField' && cell.firstChild.value) {
                                        newRowData[fieldName] = convertStringToIntegerArray(cell.firstChild.value);
                                    } else if(fieldDataType === 'ForeignKey' || fieldDataType === 'OneToOneField') {
                                        newRowData[fieldName] = convertToValidData(cell.firstChild.value, 'integer');
                                    } else if (cell.firstChild.value){
                                        newRowData[fieldName] = convertToValidData(cell.firstChild.value, fieldDataType);
                                    }    
                                }
                            }
                        }
                    });
                    
                    // Finalize sending rowData to the server
                    let application = table['model_info']['app'];
                    let model = table['model_info']['name'];
                    let body = {
                        application: application,
                        model: model,
                        data: newRowData
                    }
                    let validation = validateRow(newRow, table['field_info']);
                    if(!validation['errorCount']) {
                        
                        try {
                            let data = await sendToServer('POST', '/table_update/', body)
                            Array.from(newRow.children).forEach((cell, index) => {
                                if (index !== 0) {
                                    const span = document.createElement('span');
                                    span.textContent = data[table['field_info'][index - 1]['name']];
                                    cell.innerHTML = '';
                                    cell.appendChild(span);
                                    cell.hasChanged = false;
                                    cell.initRelateValue = span.textContent;
                                }
                            });

                            message = "Upload data successfully!";

                            // Adding first cell control buttons
                            let icon1 = controlRow(table, data, newRow, newRow.firstChild)
                            
                            newRow.className = "";

                            addRowButton.isAddingRow = false;
                            addRowButton.disabled = false;
                            
                            sessionStorage.removeItem(keyName); // Pagination handling permision

                        } catch(error) {
                            
                            // Data send to server Rejected or stablize handling issues.
                            message = 'Error in new row handling. Unknown server error!';
                            console.error(`Error in new row handling. ${error}`);
                        };
                    } else {
                        message = validation;
                        timeOut = 7 * validation.errorCount;
                    }
                    $('#confirmationModal').modal('hide');
                }}
            };
            await showConfirmationModal(`Uploading this row to server?`, 'Comfirmation!', modalButtons);

        } else {
            message = 'No changes detected at all!'
        }
        if (message) {
            showAlertTooltip(newRow.firstChild, message, timeOut ? timeOut : 5);
        }
    });

    // Cancel row data
    icon.addEventListener('click', async () =>{
        let tag;
        if (newRow.classList.contains('table-warning')) {
            const modalButtons = {
                'cancelButton': { text: 'Cancel', clickFunction: () => {
                    $('#confirmationModal').modal('hide');
                }},
                'confirmButton': { text: 'Confirm', clickFunction: () => {
                    message = "New row canceled!"
                    addRowButton.isAddingRow = false;
                    addRowButton.disabled = false;
                    if (icon.parentElement.parentElement.nextElementSibling) {
                        tag = icon.parentElement.parentElement.nextElementSibling.firstChild;
                    } else if (icon.parentElement.parentElement.previousElementSibling) {
                        tag = icon.parentElement.parentElement.previousElementSibling.firstChild;
                    } else {
                        tag = addRowButton;
                    }
                    
                    tbody.removeChild(newRow);
                    sessionStorage.removeItem(keyName);        
                    $('#confirmationModal').modal('hide');
                }}
            };
            await showConfirmationModal(`<p>Are you sure you want to miss these changes?</p><p>No undo available!</p>`,
                 'Warning!', modalButtons);
            if (message) {
                showWarningTooltip(tag, message);
            }
        } else {
            addRowButton.isAddingRow = false;
            addRowButton.disabled = false;
            tbody.removeChild(newRow);
            sessionStorage.removeItem(keyName);        
        }
    });
}

// Creating new cells under edition
function createEditingField(table, field, bodyRow, td, keyName) {
    if (field['editable'] && field['type'] !== 'AutoField') {
        // Initialize
        let input, select;
        let initText;
        initText = td.initRelateValue;
        initText = (initText === undefined || initText === null) ? "" : initText;

        if (field['relationType']) { 
            input = document.createElement('input');
            input.type = 'text';
            input.className = 'form-control';
            input.readOnly = true;
            input.value = initText;

            if (!td.classList.contains('related-field')) {
                td.classList.add('related-field');
            }
            td.dataset.relatedInfo = JSON.stringify(field['relationType']);
            
            if (!td.relationModalClickEvent) {
                td.addEventListener('click', () => {
                    relationModal(table['model_info'], field, bodyRow, td, true);
                });
            }
                td.relationModalClickEvent = true;

            // بررسی شرط null بودن
            if (!field['nullable']) {
                input.setAttribute('required', true);
            }

            input.addEventListener('input', function() {
                if (input.value == initText) {
                    td.hasChanged = false;
                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        

                } else {
                    td.hasChanged = true;
                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        

                }
                
                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }    

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }    

                    sessionStorage.removeItem(keyName);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    this.setCustomValidity('This field should not be null.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });

        } else if (field['choices']) {  // Inital data list
            select = document.createElement('select');
            select.className = 'form-control';

            let isOptionAvailable;
            try {
                isOptionAvailable = field.choices.some(choice => choice.value === initText);
            } catch {
                isOptionAvailable = false;
            }

            if (!field['nullable']) {
                select.setAttribute('required', true);
            }

            let defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select One';
            defaultOption.selected = true;
            if (select.getAttribute('required')) {
                defaultOption.setAttribute('selected', true);
            }
            select.appendChild(defaultOption);
            
            for (let choice of field.choices) {
                let option = document.createElement('option');
                option.value = choice.value;
                option.text = choice.label;
                if (choice.value === initText && isOptionAvailable) {
                    option.selected = true;
                }
                select.appendChild(option);
            }

            select.addEventListener('change', function() {
                if (select.value == initText) {
                    td.hasChanged = false;

                    if (this.classList.toggle('is-valid')) {
                        this.classList.remove('is-valid');
                    }
                } else {
                    td.hasChanged = true;
                    
                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }
                }

                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }
                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }
                    sessionStorage.setItem(keyName, false);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    this.setCustomValidity('Please choose valid item.');
                } else {
                    this.classList.remove('is-invalid');
                }
                this.reportValidity();
            });

        } else if (field['type'].toLowerCase().includes('datetime')) {
            input = document.createElement('input');
            input.type = 'datetime-local';
            input.className = 'form-control';
            input.value = initText;

            // بررسی شرط null بودن
            if (!field['nullable']) {
                input.setAttribute('required', true);
            }

            input.addEventListener('input', function() {
                if (input.value == initText) {
                    td.hasChanged = false;

                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        

                } else {
                    td.hasChanged = true;

                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        
                }

                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }

                    sessionStorage.removeItem(keyName);
                }

                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    // پیغام مناسب برای ورود داده نامعتبر
                    this.setCustomValidity('Please enter a valid date and time.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });
        } else if (field['type'].toLowerCase().includes('boolean')) {
            initText = String(initText);
            select = document.createElement('select');
            select.className = 'form-control';

            let isOptionAvailable;
            try {
                isOptionAvailable = ['true', 'false'].some(choice => choice == initText);
            } catch {
                isOptionAvailable = false;
            }
            
            // بررسی شرط null بودن
            if (!field['nullable']) {
                select.setAttribute('required', true);
            }
            
            let defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select One';
            defaultOption.selected = true;
            if (select.getAttribute('required')) {
                defaultOption.setAttribute('selected', true);
            }
            select.appendChild(defaultOption);

            ['true', 'false'].forEach(condition => {
                let option = document.createElement('option');
                option.value = condition;
                option.text = condition;
                if (condition === initText && isOptionAvailable) {
                    option.selected = true;
                }
                select.appendChild(option);    
            });

            select.addEventListener('change', function() {
                if (select.value == initText) {
                    td.hasChanged = false;

                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        

                } else {

                    td.hasChanged = true;

                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        
                }
                
                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }

                    sessionStorage.removeItem(keyName);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    // پیغام مناسب برای ورود داده نامعتبر
                    this.setCustomValidity('Only permited boolean value.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });
        } else if (field['type'].toLowerCase().includes('int')) {
            input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.min = 0;
            input.style.width = "70px";
            input.value = initText;
        
            // بررسی شرط null بودن
            if (!field['nullable']) {
                input.setAttribute('required', true);
            }
        
            input.addEventListener('input', function() {
                if (input.value == initText) {
                    td.hasChanged = false;
                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        

                } else {
                    td.hasChanged = true;
                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        
                }
                
                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }    

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }    

                    sessionStorage.removeItem(keyName);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    // پیغام مناسب برای ورود داده نامعتبر
                    this.setCustomValidity('Please enter a valid small integer.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });
        } else if (field['type'].toLowerCase().includes('float')) {
            input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.value = initText;

            input.setAttribute('pattern', '\\d+(\\.\\d+)?'); // بررسی الگوی اعداد اعشاری
            input.setAttribute('title', 'Please enter a valid decimal number.'); // پیام مربوط به ورود داده نامعتبر
            
            // بررسی شرط null بودن
            if (!field['nullable']) {
                input.setAttribute('required', true);
            }
        
            input.addEventListener('input', function() {
                if (input.value == initText) {
                    td.hasChanged = false;
                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        


                } else {
                    td.hasChanged = true;
                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        
                }
                
                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }    

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }

                    sessionStorage.removeItem(keyName);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    // پیغام مناسب برای ورود داده نامعتبر
                    this.setCustomValidity('Please enter a valid decimal number.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });
        } else {
            // ایجاد ویژگی‌های دیگر برای سایر نوع‌های داده
            input = document.createElement('input');
            input.type = 'text';
            input.className = 'form-control';
            input.value = initText;

            // بررسی شرط null بودن
            if (!field['nullable']) {
                input.setAttribute('required', true);
            }

            input.addEventListener('input', function() {
                if (input.value == initText) {
                    td.hasChanged = false;
                    if (this.classList.contains('is-valid')) {
                        this.classList.remove('is-valid');
                    }                        

                } else {
                    td.hasChanged = true;
                    if (!this.classList.contains('is-valid')) {
                        this.classList.add('is-valid');
                    }                        

                }
                
                // If is there a changed cell all ever.
                if (Array.from(bodyRow.querySelectorAll('td')).filter(td => td.hasChanged === true).length) {
                    if (!bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.add('table-warning');
                    }
                    if (bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.remove('table-active');
                    }    

                    sessionStorage.setItem(keyName, true);

                } else {

                    if (bodyRow.classList.contains('table-warning')) {
                        bodyRow.classList.remove('table-warning');
                    }
                    if (!bodyRow.classList.contains('table-active')) {
                        bodyRow.classList.add('table-active');
                    }    

                    sessionStorage.removeItem(keyName);
                }
                
                this.setCustomValidity('');
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    this.setCustomValidity('This field should not be null.');
                } else {
                    this.classList.remove('is-invalid');
                    this.setCustomValidity('');
                }
                this.reportValidity();
            });
        }

        td.innerHTML = '';
        if (input instanceof HTMLElement) {
            td.appendChild(input);
        } else if (select instanceof HTMLElement) {
            td.appendChild(select);
        }
        // td.firstChild.className = "max-width-element";
    }
}

function validateRow(bodyRow, fieldsList) {
    const errors = []; // آرایه‌ای برای ذخیره خطاها
    const validationReport = []; // گزارش اعتبارسنجی

    const tds = bodyRow.getElementsByTagName('td');
    for (let i = 1; i < tds.length; i++) { // شماره‌گذاری از 1 به جای 0
        const td = tds[i];
        if (fieldsList[i - 1]['editable'] && fieldsList[i - 1]['type'] !== 'AutoField') {

            if (td.firstElementChild instanceof HTMLInputElement) {

                const input = td.firstElementChild
    
                if (input.getAttribute('required') && input.value.trim() === '') {
                    if (input.type === 'checkbox') {
                        continue;
                    }
                    const fieldName = fieldsList[i - 1]['name']; // مشخص کردن نام فیلد خطا دار
                    errors.push({
                        index: fieldName,
                        message: 'Field not nullable!',
                    });
        
                    input.classList.add('is-invalid');
                    input.setAttribute('data-bs-toggle', 'tooltip');
                    input.setAttribute('data-bs-placement', 'top');
                } else if (input.classList.contains('is-invalid')) {
                    const fieldName = fieldsList[i - 1]['name']; // مشخص کردن نام فیلد خطا دار
                    errors.push({
                        index: fieldName,
                        message: 'Invalid input',
                    });
        
                    input.classList.add('is-invalid');
                    input.setAttribute('data-bs-toggle', 'tooltip');
                    input.setAttribute('data-bs-placement', 'top');
                }    
            }            
        }
    }

    // تولید گزارش
    if (errors.length > 0) {
        validationReport.push('Validation Errors:');
        errors.forEach((error) => {
            validationReport.push(`Error at (${error.index}) field: ${error.message}`);
        });
    } else {
        validationReport.push('Validation Passed: No errors found.');
    }

    // برگرداندن شمارش خطاها و گزارش اعتبارسنجی
    return {
        errorCount: errors.length,
        validationReport: validationReport,
    };
}


// Specialist functions
function paginationPositions ({ul, liFirst, aFirst, spanFirst, liPrevious, aPrevious, spanPrevious, currentPage,
     li, a, liNext, aNext, spanNext, liLast, aLast, spanLast, count, url, firstPage = 1, numOfPages}) {
    
    // Initializations
    ul.innerHTML = "";
    currentPage = Number(currentPage);
    count = Number(count);

    const btnNum = li.length - 1; // Number of Buttons

    // Before
    liFirst.innerHTML = "";
    liPrevious.innerHTML = "";

    if (currentPage > 1) {

        liFirst.className = 'page-item';
        liPrevious.className = 'page-item';

        aFirst.href = `${paginatorUrlCreator(url, firstPage)}`;
        aPrevious.href = `${paginatorUrlCreator(url, currentPage - 1)}`;

        aFirst.innerText = `First(${firstPage})`;
            
        liFirst.appendChild(aFirst);
        liPrevious.appendChild(aPrevious);
    
    } else {
        liFirst.className = 'page-item disabled';
        liPrevious.className = 'page-item disabled';

        spanFirst.innerText = `First(${firstPage})`;

        liFirst.appendChild(spanFirst);    
        liPrevious.appendChild(spanPrevious);
    }
    ul.appendChild(liFirst);
    ul.appendChild(liPrevious);

    // Numeral buttons preparation
    let suprimum = currentPage + Math.min((count - currentPage), Math.floor((btnNum - 1) / 2));
    let offset = -Math.min(suprimum - Math.min(btnNum, count), 0);
    let infimum = Math.max(suprimum - (btnNum - 1), 1);
    suprimum += offset;

    for(var i = infimum, k = 1; i < currentPage; i++, k++) {
        a[k].textContent = i;
        a[k].href = `${paginatorUrlCreator(url, i)}`;
        ul.appendChild(li[k]);
    }

    // Current Page
    if(btnNum > 0) {
        let spanCrtBtn = li[btnNum].querySelector('a span'); // Span Current Button
        spanCrtBtn.textContent = i;
        ul.appendChild(li[btnNum]);
    }

    for(let j = i + 1, k2 = k; j <= suprimum ; j++, k2++) {
        a[k2].textContent = j;
        a[k2].href = `${paginatorUrlCreator(url, j)}`;
        ul.appendChild(li[k2]);
    }

    // After
    liNext.innerHTML = "";
    liLast.innerHTML = "";
    
    if (currentPage < count) {

        liNext.className ='page-item';
        liLast.className  = 'page-item';

        aNext.href = `${paginatorUrlCreator(url, currentPage + 1)}`;
        aLast.href = `${paginatorUrlCreator(url, count)}`;

        aLast.innerText =`Last(${count})`;
        
        liNext.appendChild(aNext);
        liLast.appendChild(aLast);
    } else {
        liNext.className = 'page-item disabled';
        liLast.className = 'page-item disabled';
        
        spanLast.innerText = `Last(${count})`

        liNext.appendChild(spanNext);
        liLast.appendChild(spanLast);    
    }
    ul.appendChild(liNext);
    ul.appendChild(liLast);

    return ul;
}

function paginationUrlInitalize(metadata) {
    // Variables declartion
    let count = Number(metadata.count);
    let currentPage = undefined;
    let url = undefined;
    let param;

    if (count > 1) {

        if (metadata.next !== null) {
            let nextUrl = new URL(metadata.next);
            let nextPage = Number(nextUrl.searchParams.get('page'));

            currentPage = nextPage - 1;
            param = nextUrl.searchParams;
            param.set('page', currentPage);
            url = nextUrl.toString();

            const perPageCount = metadata['results'].length;
            const numOfPages = Math.ceil(count / perPageCount);
            count = numOfPages;

        } else if (metadata.previous !== null){
            let previousUrl = new URL(metadata.previous);
            let previousPage = Number(previousUrl.searchParams.get('page'));
            
            currentPage = previousPage + 1;
            param = previousUrl.searchParams;
            param.set('page', currentPage);
            url = previousUrl.toString();

            count = currentPage;
        } else {
            count = 1;
            currentPage = 1;
        }

    } else {

        if (!count) {count = 0;}

        currentPage = count;

    }

    let result = {
        count, // Means count of pages at all
        currentPage,
        url // url of current page
    };
    
    return result;
}

function paginationDomCreator(numButtons) {

    // Variable declaration and initialization
    let li = [];
    let a = [];

    // DOM elements holder
    let ul = document.createElement('ul');
    ul.className = 'pagination';

    // First
    let liFirst = document.createElement('li');
    let aFirst = document.createElement('a');
    aFirst.className = 'page-link';
    let spanFirst = document.createElement('span');
    spanFirst.className = 'page-link';

    // Previous
    let liPrevious = document.createElement('li');
    let aPrevious = document.createElement('a');
    aPrevious.className = 'page-link';
    aPrevious.innerText = 'Previous';
    let spanPrevious = document.createElement('span');
    spanPrevious.className = 'page-link';
    spanPrevious.innerText = 'Previous';
    

    // Next
    let liNext = document.createElement('li');
    let aNext = document.createElement('a');
    aNext.className = 'page-link';
    aNext.innerText = 'Next';
    let spanNext = document.createElement('span');
    spanNext.className = 'page-link';
    spanNext.innerText = 'Next';

    // Last
    let liLast = document.createElement('li');
    let aLast = document.createElement('a');
    aLast.className  ='page-link';
    aLast.innerText = 'Last';
    let spanLast = document.createElement('span');
    spanLast.className = "page-link";
    spanLast.innerText = 'Last';

    if (numButtons > 0) {

        // Create buttons
        for (let i = 1; i <= numButtons; i++) {
            li[i] = document.createElement('li');
            li[i].className = 'page-item';
            
            a[i] = document.createElement('a');
            a[i].className = 'page-link';

            li[i].appendChild(a[i]);
        }

        // preparing Selected button specialists
        li[numButtons].className = 'page-item active';
        li[numButtons].setAttribute('aria-current', 'page');

        let spanSelBtn = document.createElement('span'); // Span Selected Button
        spanSelBtn.className = 'sr-only';
        spanSelBtn.innerText = '(current)';
        spanSelBtn.style = 'display: none';

        let spanSelHldr = document.createElement('span'); // Span Selected Holder
        spanSelHldr.className = 'page-link';

        a[numButtons].href = '#';
        a[numButtons].appendChild(spanSelHldr);
        a[numButtons].appendChild(spanSelBtn);

    }
        let elements = {
            ul,
            liFirst,
            aFirst,
            spanFirst,
            liPrevious,
            aPrevious,
            spanPrevious,
            li,
            a,
            liNext,
            aNext,
            spanNext,
            liLast,
            aLast,
            spanLast,
        };
        
    return elements;

}

function paginatorUrlCreator (url, page) {
    url = new URL(url);
    let param = url.searchParams;
    param.set('page', page);
    const newUrl = url.toString();

    return newUrl;
}

async function pagination (id, metadata, numButtons=3, func, source = undefined) {

    // Variable Initalization
    let pI;
    let dom;
    let elements;
    let url;

    let nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Count of exist tables Pagination');

    pI = paginationUrlInitalize(metadata);
    
    dom = paginationDomCreator(numButtons);

    elements = {...dom, ...pI};
        
    nav.appendChild(paginationPositions(elements));

    // <a> elements event listener
    let aElements = [dom.aFirst, dom.aPrevious, dom.aNext, dom.aLast, ...dom.a];
    aElements.forEach( a => {
        if (a) {
            a.addEventListener('click', async event => {
                // event.stopPropagation();
                event.preventDefault();
                try {
                    let keyName = `editingTable_${source['appModel']['application']}_${source['appModel']['model']}`;
                    keyName = keyName.toLowerCase();
                    if (sessionStorage.getItem(keyName)) {

                        const paginationWarn = {
                            'cancelButton': { text: 'Cancel',
                             clickFunction: () => {
                                $('#confirmationModal').modal('hide');
                            } },
                            'confirmButton': { text: 'Confirm', clickFunction: () => {
                                sessionStorage.removeItem(keyName);
                                $('#confirmationModal').modal('hide');
                            } }
                        };

                        await showConfirmationModal(`The table involves row(s) that are under editing.<br> 
                        Changing the table page before saving them will loose what are currently in change.<br>
                        Are you sure?`, 'Confirmation!', paginationWarn);
                    }
                    if (sessionStorage.getItem(keyName)) {
                        return;
                    }    
                } catch {
                }
                try {
                    url = new URL(event.target.href);
                    
                }
                catch {
                    return;
                }

                let param = url.searchParams;
                let page = param.get('page');

                localStorage.setItem(id, page);

                elements.currentPage = page;

                nav.innerHTML = "";
                nav.appendChild(paginationPositions(elements));

                if (typeof func === "function") {
                    var args = [url.toString()];
                    if (source !== undefined) {
                      args = args.concat(Object.values(source));
                    }
                    func.apply(null, args);
                } else {
                    console.error("Pagination: Provided argument is not a function");
                }
            });    
        }
    });

    return nav;
}

function createDynamicTable(table) {
    let keyName = `editingTable_${table['model_info']['app']}_${table['model_info']['name']}`;
    keyName = keyName.toLowerCase();
    window.onbeforeunload = function() {
        sessionStorage.removeItem(keyName);
    }

    // Create table elements
    const tableElement = document.createElement('table');
    tableElement.className = "table table-bordered"; // Bootstrap classes
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create header row
    const headerRow = document.createElement('tr');
    
    // Create New empty row
    const th = document.createElement('th');
    const addRowButton = document.createElement('button');

    addRowButton.innerText = 'Add Row';
    addRowButton.className = 'add-row-btn';
    addRowButton.id = 'setting-add-row-btn';
    addRowButton.classList.add('btn', 'btn-primary');
    
    th.appendChild(addRowButton)
    headerRow.appendChild(th);

    addRowButton.addEventListener('click', () => {
        // Enable/disable the add row button based on empty rows
        if (addRowButton.isAddingRow) {
            addRowButton.disabled = true;
            return;
        };
        addRowButton.isAddingRow = true;
        addRowButton.disabled = true;
        
        createNewRow(table, tbody, addRowButton, keyName);
        // tbody.appendChild(newRow);
    });
    
    // Create table headers
    for (let i = 0; i < table['field_info'].length; i++) {
        let field = table['field_info'][i];
        let nextField = i < table['field_info'].length - 1 ? table['field_info'][i + 1] : null;

        const th = document.createElement('th');
        th.innerText = field.verbose_name;

        const iconEyeSlash = document.createElement('i');
        iconEyeSlash.classList.add('fas', 'fa-eye-slash');

        headerRow.appendChild(th);

        if (field.name === 'created_at' || field.name === 'updated_at' || field.name === 'deleted_at') {
            th.classList.add('hidden');
            th.previousElementSibling.prepend(iconEyeSlash);
        }
        th.classList.add('clickable');
        if (nextField) {
            th.title = `Click to toggle hide / unhide next column -> (${nextField.verbose_name})`;
        }
        th.addEventListener('click', function(event) {
            // Get the index of the next th in the row
            let index = Array.from(th.parentNode.children).indexOf(th) + 1;
        
            // Select the next th and toggle its visibility
            let nextTh = th.parentNode.children[index];
            if (nextTh) {
                nextTh.classList.toggle('hidden');

                let hasIcon = Array.from(th.children).some(child => 
                    child.classList.contains('fas') && 
                    child.classList.contains('fa-eye-slash')
                );

                if (nextTh.classList.contains('hidden')) {
                    if (!hasIcon) {
                        th.prepend(iconEyeSlash);
                    }
                } else {
                    if (hasIcon) {
                        th.removeChild(th.firstChild);
                    }
                }
        
                // Select all td elements in the same column and toggle their visibility
                document.querySelectorAll(`td:nth-child(${index + 1})`).forEach(td => {
                    td.classList.toggle('hidden');
                });
            }
        });
    };
    thead.appendChild(headerRow);
    tableElement.appendChild(thead);
    
    // Create body rows
    if (table['model_instances']['results']) {
        table['model_instances']['results'].forEach(record => {

            const bodyRow = document.createElement('tr');
            const td = document.createElement('td');
    
            // Adding first cell control buttons
            let icon1 = controlRow(table, record, bodyRow, td)
    
            bodyRow.appendChild(td);
    
            // Creating body row data cells
            table['field_info'].forEach((field, index) => { // Using field_info to iterate through all fields
                const td = document.createElement('td');
                td.className = "max-width-cell";
    
                const span = document.createElement('span');
                span.className = "max-width-element";
                
                // let spacedNumbers = convertToString(record[field['name']]).replace(/,/g, ', ');

                span.textContent = record[field['name']];
                td.appendChild(span);
                td.initRelateValue = convertToString(record[field['name']]);
    
                if (field.name === 'created_at' || field.name === 'updated_at' || field.name === 'deleted_at') {
                    td.classList.add('hidden');
                }
    
                if (field['relationType']) {
    
                // if the field is a related
                if (!td.classList.contains('related-field')) {
                    td.classList.add('related-field');
                }
                td.dataset.relatedInfo = JSON.stringify(field['relationType']);
                
                    if (!td.relationModalClickEvent) {
                        td.addEventListener('click', () => {
                            relationModal(table['model_info'], field, bodyRow, td);
                        });
                        td.relationModalClickEvent = true;
                    }
                }
                bodyRow.appendChild(td);
            });
            tbody.appendChild(bodyRow);
        });    
    }
    tableElement.appendChild(tbody);

    // Return table DOM
    return tableElement;
}

async function refreshBotton(appModel, icon, container) {
    
    // Variables decralation and initialization
    let img;
    let msg;
    let warningDisplayed = false;

    // Perform table Header
        img = document.createElement('img');
        img.className = "clickable";
        img.src = icon;
        img.style.width = "20px";
        img.style.display = "inline";
        img.title = 'Refresh table data';

        // Refresh table
        img.addEventListener('click', async () => {
            if (container.style.display == 'block') {
                if (container.innerHTML != "") {
                    if (confirm("Do you want to proceed?")) {
                        // temp = container.cloneNode(true);
                        let msgElm = container.querySelector('h5');
                        if (msgElm) {
                            container.children[1].remove();
                        } else {
                            container.children[0].remove();
                        }
                        // container.classList.add('blur-anymate-class');

                        let page = localStorage.getItem(`${appModel.application}_${appModel.model}`);
                        page = page ? page : 1;

                        let result = await getTableContent(appModel.application, appModel.model, page);
                        // await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
                        void container.offsetWidth;
                        container.classList.remove('blur-anymate-class');
                        if (result != null) {
                            let tableObject = createDynamicTable(result);
                            tableObject.classList.add('settingTable');
                            container.insertBefore(tableObject, container.firstElementChild);
                        } else {
                            // container.parentNode.replaceChild(temp, container);
                            // container = document.querySelector(`#self_${appModel.application}${appModel.model}`);
                            
                            if (! msgElm) {
                                msg = document.createElement('h5');
                                msg.className = "alert alert-warning";
                                msg.textContent = "The table not updated! Connection loss.";    
                                // container.insertBefore(msg, container.firstChild);
                                container.appendChild(msg);
                            }
                        }    
                    } else {
                        // console.log("No table refreshed!");
                    }                    
                }
            }
        });

        return img;
}

// Get tables index from appropriate model id
async function getTablesIndex(id, page=1) {
    let tablesInd = await getFromServer(`tables_index_from_menus_record/${id}`, `page=${page}`);
    if (!tablesInd) {
        console.log('No Tables index data received!');
    } else if ('detail' in tablesInd) {
        console.log('Error fetching tables index: ' + tablesInd.detail);
    } else {
        return tablesInd;
    }
}

// Get table title
async function getTableAppModel(id) {
    const appModel = await getFromServer(`table_app_model/${id}`);
    if (!appModel) {
        console.log('No Table title data received!');
    } else if ('detail' in appModel) {
        console.log('Error fetching table title: ' + appModel.detail);
    } else {
        return appModel;
    }
}

// Get Table's appropriated header
async function getHeader (appModel, container) {

    let tableHeader = createTableTitle(appModel);

    // Table header triggres table contents visible or hide
    tableHeader.addEventListener('click', async () => {
        if (container.style.display == 'none') {
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    });
    
    return tableHeader;    
}

// The container which involve table title and its body container
function createHoleTableContainer(tableTitle) {
    const subContainer = document.createElement('div');
    subContainer.className = "hole-table-container";
    subContainer.id = "hole_" + tableTitle.application + tableTitle.model;
    
    return subContainer;
}

// The container which involve table body
function createSelfTableContainer(tableTitle) {
    const subContainer = document.createElement('div');
    subContainer.className = "self-table-container";
    subContainer.id = "self_" + tableTitle.application + tableTitle.model;
    
    return subContainer;
}

// Table title
function createTableTitle(appModel) {
    const title = document.createElement('h2');
    title.className = "clickable";
    title.innerHTML = "<span class='text-primary'>Application Name: </span>" + 
    appModel.application + 
    " | " +
    "<span class='text-success'>Model Name: </span>" + 
    appModel.model;
    
    return title;
}

// Draw table
async function getTableContent(app, model, page=1, pageSize=10) {
    const url = `serialized_table/${app}/${model}`;
    let table = await getFromServer(url, `page=${page}&page_size=${pageSize}`);
    
    if (!table) {
        console.log('No Table content data received!');
    } else if ('detail' in table) {
        console.log('Error fetching table content: ' + table.detail);
    } else {
        return table;
    }   
}

async function aggregateTablesData(metadata, page=1) {
    
    const container = document.createElement('div');
    container.id = "sub-tables-container"

    await Promise.all(metadata['results'].map(async index => {
        let tableInd = index.id; // Table's Index

        // Variables decralation and initialization
        let tableObject;
        const br = document.createElement('br');

        let appModel = await getTableAppModel(tableInd);

        // Collecting table equipes TAG        
        let tableSelfContainer = createSelfTableContainer(appModel);
        tableSelfContainer.style.display = 'none';
        
        let tableHoleContainer = createHoleTableContainer(appModel);

        // Initially fetch table contents
        getTableContent(appModel.application, appModel.model).then(result => {
            let tableObject = createDynamicTable(result);
            let metadata = result['model_instances'];
            if (tableObject != null) {

                tableObject.classList.add('settingTable');

                // append table contents to tableSelfContainer element
                tableSelfContainer.appendChild(tableObject);

                // Initialize page number
                localStorage.setItem(`${appModel.application}_${appModel.model}`, 1);

                // Inner table Pagination
                pagination(`${appModel.application}_${appModel.model}`, metadata, 3, tablePageUpdater, {appModel, tableSelfContainer})
                .then(node => tableSelfContainer.appendChild(node));

                let hr = document.createElement('hr');
                tableSelfContainer.appendChild(hr);

            } else {
                console.log("Error!, Table content note cached.");
            }
        });        

        let tableHeader = await getHeader(appModel, tableSelfContainer);
        tableHeader.style.display = "inline";

        const img = await refreshBotton(appModel, logoIconPic, tableSelfContainer);

        // Perform tableHoleContainer tag
        tableHoleContainer.appendChild(tableHeader);
        tableHoleContainer.appendChild(tableSelfContainer);

        // Nabouring refersh logo and Table Header line breaker
        tableHeader.insertAdjacentElement('afterend', img);
        img.parentNode.insertBefore(br, img.nextSibling);         
        container.appendChild(tableHoleContainer);
    }));

    return container;

}

async function tableAndPagination (id, page=1) {

    const container = document.getElementById('tables-container');
    if (!container) {
        return;
    }
    
    container.innerHTML = "";

    let metadata = await getTablesIndex(id, page);
    
    // Tables
    container.appendChild(await aggregateTablesData(metadata));

    let hr = document.createElement('hr');
    hr.style.borderTop = "3px solid black";
    // hr.style.marginTop = "-1px";
    container.appendChild(hr);

    // Pagination
    pagination(id, metadata, 3, tablesPageUpdater).then(node => container.appendChild(node));
    // container.appendChild(pagination(id, metadata, 3, tablesPageUpdater));
}

async function tablesPageUpdater(url) {

    try {
        url = new URL(url);
        
    }
    catch {
        return;
    }

    let path = url.pathname;
    let id = path.split('/')[2];

    let param = url.searchParams;
    let page = param.get('page');

    const container = document.getElementById('tables-container');

    container.firstChild.innerHTML = "";

    let metadata = await getTablesIndex(id, page);

    let tables = await aggregateTablesData(metadata);

    container.firstChild.appendChild(tables);
}

async function tablePageUpdater (url, appModel, tableSelfContainer) {

    try {
        url = new URL(url);
        
    }
    catch {
        return;
    }

    let param = url.searchParams;
    let page = param.get('page');

    let tableElement = tableSelfContainer.firstElementChild;
    tableElement.remove();

    const result = await getTableContent(appModel.application, appModel.model, page);

    let tableObject = createDynamicTable(result);
    tableObject.classList.add('settingTable');

    tableSelfContainer.insertBefore(tableObject, tableSelfContainer.firstElementChild);
}

// SPA block handler
function SPAFrame(tag, title, url="") {
    localStorage.setItem(SESSION_TAG_KEY, tag);
    localStorage.setItem(SESSION_PAGE_KEY, title);
    if (isUserAuthenticated) {
        sendToServer('POST', `/set_session/${SESSION_TAG_KEY}/${tag}/`, `key: ${tag}`);
        sendToServer('POST', `/set_session/${SESSION_PAGE_KEY}/${title}/`, `key: ${title}`);    
    }
    if (!url) {
        url = localStorage.getItem('first_url');
    }

    if(!title) {title = 'home';}
    title = title.split(', ');

    const displayValue = elm => {
        if (elm.classList.contains('SPA')) {
            return title.every(className => elm.classList.contains(className)) ? 'block' : 'none';    
        }
    };

    document.querySelectorAll('*').forEach(elm => {
        elm.style.display = displayValue(elm);
    });
    switch(tag + title) {
        case 'sectionhome':
            console.log("Home");
            break;
        case 'sectionsettings':
            // console.log("Settings");
            savedId = localStorage.getItem(SESSION_ID_KEY);
            console.log(savedId);
            let title = localStorage.getItem('settingMenuTrail');
            if (title && document.querySelector('#settings')) {
                document.querySelector('#settings').innerText = title;
            }
            tableAndPagination(savedId);
            break;
        case "articlefirst_present":
            const holder = document.querySelector('#website_container');
            holder.innerHTML = "";
            let iframe = document.createElement('iframe');
            holder.appendChild(iframe);
            iframe.width = "1000";
            iframe.height = "800";
            iframe.src = url;
            break;
        default:
            console.error('Unknown page!');
            savedPage = "home";
            savedTag = "section";
            SPAFrame(savedTag, savedPage);
    }
}

// Current page Server session checking
async function initializePageServer() {
    try {
        // Default SPA Selector or recent one
        savedPage = localStorage.getItem(SESSION_PAGE_KEY);
        savedTag = localStorage.getItem(SESSION_TAG_KEY);
        if (!savedPage || !savedTag) {
            if (isUserAuthenticated) {
                savedPage = await getFromServer(`get_session/${SESSION_PAGE_KEY}`).value;
                savedTag = await getFromServer(`get_session/${SESSION_TAG_KEY}`).value;        
            }
            if (!savedPage || !savedTag) {
                savedPage = "home";
                savedTag = "section";
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }    
}

// Menus onclick event
function menusOnClick() {
    document.querySelectorAll('a.menu').forEach(tag => {
        const id = tag.getAttribute('data-id');
        const url = tag.getAttribute('data-url');
        const holder = tag.getAttribute('data-tag');
        const option = tag.getAttribute('data-page');

        tag.addEventListener('click', event => {

            event.preventDefault();

            let settingMenuTrail = getMenuTrail(tag);
            localStorage.setItem('settingMenuTrail', settingMenuTrail);
            localStorage.setItem('first_url', url);

            localStorage.setItem(SESSION_ID_KEY, id);
            SPAFrame(holder, option, url);
        });
    });
}

// Load lazy images
function imagesLazyLoad() {
    const lazyImages = document.querySelectorAll(".lazy-load");
    lazyImages.forEach(img => {
        img.src = img.getAttribute("data-src");
        img.onload = () => img.classList.add("loaded");
    });    
}

// Initialize Swiper
function initSwiper() {
    const swiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: { delay: 10000 },
        navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            renderBullet: (index, className) => `<span class="${className}"></span>`,
            dynamicBullets: true,
        },
    });
}

document.addEventListener('DOMContentLoaded', async () => {

    await refreshToken()
    imagesLazyLoad();
    initSwiper();
    menusOnClick();
    await initializePageServer();
    SPAFrame(savedTag, savedPage);

});