import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import ReactDOM from "react-dom";
import { useTable, usePagination, useFilters, useRowSelect } from 'react-table';
import { Table, Modal, Button, Form, Alert, Card, Overlay } from 'react-bootstrap';
import { FaCog, FaSave, FaTimes, FaTrashAlt } from 'react-icons/fa';


const TModal = ({ elm, onClose, app, editable, model }) => {
  const [show, setShow] = useState(true);
  const [enterClicked, setEnterClicked] = useState(false);
  const [selectedIdParent, setSelectedIdParent] = useState("");
  const clonedElm = React.cloneElement(elm, { enterClicked: enterClicked, setSelectedIdParent: setSelectedIdParent });
  
  const handleClose = () => setShow(false);
  const handleModalClick = (e) => {
    e.stopPropagation();
  };

  const handleOutsideClick = (e) => {
    if (e.target === e.currentTarget) {
      setShow(false);
    }
  };

  const handleEnterExit = () => {
    handleClose()
  }

  useEffect(() => {
    return () => {
      onClose();
    };
  }, [onClose]);

  const modalBodyStyle = {
    maxHeight: window.innerWidth > 768 ? 'calc(100vh - 210px)' : 'calc(100vh - 110px)',
    maxWidth: window.innerWidth > 768 ? 'calc(100vw - 210px)' : 'calc(100vw - 110px)',
    overflowY: 'auto',
    overflowX: 'auto',
  };

  return (
    <>
      <Modal show={show} onHide={handleClose} backdrop="static">
        <div onClick={handleOutsideClick}>
          <Modal.Header closeButton>
          <Modal.Title>
            <div><FaCog /> Application: ({app})</div>
            <div>     Model:  ....   ({model})</div>
          </Modal.Title>
          </Modal.Header>
          <Modal.Body style={modalBodyStyle}>
            {clonedElm}
            <Form>
              <Form.Group controlId="exampleForm.ControlTextarea1">
              <Card.Title style={{ marginTop: '20px' }}>Selected IDs</Card.Title>
                <Alert variant="info">
                  The IDs displayed here are currently selected. Please note that some selected IDs might not be visible in the current table page due to pagination.
                </Alert>
              <Form.Control as="textarea" rows={1} value={selectedIdParent} readOnly />
            </Form.Group>              
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              <FaTimes /> Close
            </Button>
            <Button variant="primary" disabled={!editable || enterClicked} onClick={() => {
              setEnterClicked(true);
              handleEnterExit();
            }}>
              <FaSave /> Enter
            </Button>
          </Modal.Footer>
        </div>
      </Modal>
    </>
  );
};


function DynamicTableComponent(props) {
  const { getTableContent, app, model, many, values, editable, enterClicked, onSelectedIdsChange, setSelectedIdParent } = props;
  
  const checkboxRef = useRef();

  // States
  let ids = Array.isArray(values) ? values : [values];
  const [selectedId, setSelectedId] = useState(ids);
  const [isFirstRender, setIsFirstRender] = useState(true);

  const [pagination, setPagination] = React.useState({
    table: null,
    currentPageIndex: 0,
    listPages: [],
    hasPreviousPage: undefined,
    hasNextPage: undefined,
  });

  // Rows selection handling
  const handleRadioClick = (id) => {
    id = [id];
    setSelectedId(id);
  };

  const handleCheckboxChange = (id) => {
    if (Array.isArray(id)) {
      if (id.length === 0) {
        // If id is an empty array, remove all ids from selectedId
        setSelectedId(selectedId.filter(element => !data.map(row => row.id).includes(element)));
      } else {
        // If id is an array of all ids, add all ids to selectedId
        setSelectedId(selectedId.concat(id.filter(element => !selectedId.includes(element))));
      }
    } else {
      // Existing code for handling a single id
      if (selectedId.includes(id)) {
        setSelectedId(selectedId.filter(element => element !== id));
      } else {
        setSelectedId(selectedId.concat(id));
      }
    }
  }

  const isIdSelected = (id) => {
    const isSelected = selectedId.includes(id);
    return isSelected;
  };

  // Initializing table data
  const columns = useMemo(() => {
    if (pagination.table === null) {
      return [];
    }
    return [
      {
        Header: 'id',
        accessor: 'id0', 
      },
      ...pagination.table.field_info
        .filter(field => !['created_at', 'updated_at', 'deleted_at'].includes(field.name))
        .map((field, index) => ({
          Header: field.name,
          accessor: field.name,
        }))
    ];
  }, [selectedId, pagination]);

  const data = useMemo(() => {
    if (pagination.table === null) {
      return [];
    }
    return pagination.table.model_instances.results.map((record, index) => {
      const row = {};
      pagination.table.field_info.forEach((field) => {
        if (field.name !== 'created_at' && field.name !== 'updated_at' && field.name !== 'deleted_at') {
          row[field.name] = record[field.name];
        }
      });
      row.id0 = index + 1;
      return row;
    });
  }, [pagination]);

  const initialSelectedRows = selectedId.reduce((acc, id) => {
    const foundIndex = data.findIndex((row) => row.id === id);
    if (foundIndex !== -1) {
        acc[foundIndex] = true;
    }
    return acc;
}, {})
  
  const initialState = {
    pageIndex: 0, 
    pageSize: 10, 
    hiddenColumns: ['id0'],
    selectedRowIds: initialSelectedRows
  }

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    getToggleAllRowsSelectedProps,
    rows,
    prepareRow,
    selectedFlatRows,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    toggleRowSelected,
    state: { pageIndex, pageSize, selectedRowIds },
  } = useTable(
    {
      columns,
      data,
      autoResetSelectedRows: false,
      initialState,
    },
    useFilters,
    usePagination,
    useRowSelect,
    hooks => {
      hooks.visibleColumns.push(columns => [
        {
          id: 'selection',
          Header: ({ getToggleAllRowsSelectedProps }) =>
            many ? (
              <input
                type="checkbox"
                disabled={!editable}
                {...getToggleAllRowsSelectedProps({
                  indeterminate: undefined,
                  onChange: (e) => {
                    const originalOnChange = getToggleAllRowsSelectedProps().onChange;
                    originalOnChange(e);
                    if (e.target.checked) {
                      const allRowIds = data.map(row => row.id);
                      handleCheckboxChange(allRowIds); // Pass all row IDs
                    } else {
                      handleCheckboxChange([]); // Pass an empty array
                    }
                  },
                })}
              
                ref={checkboxRef}
              />
            ) : null,
          Cell: ({ row }) => (
            many ? (
              <input
                type='checkbox'
                disabled={!editable}
                {...row.getToggleRowSelectedProps({
                  indeterminate: undefined,
                  onChange: (e) => {
                    const originalOnChange = row.getToggleRowSelectedProps().onChange;
                    originalOnChange(e);
                    handleCheckboxChange(row.original.id);
                  },
                })}
              /> 
            ) : (
              <input
                type='radio'
                checked={isIdSelected(row.original.id)}
                onChange={() => handleRadioClick(row.original.id)}
                disabled={!editable}
              />
            )
          ),
        },
        ...columns,
      ]);
    }    
  );
  
  // Counts numbers in an array based on their relation to a given reference number
  function countNumbers(array, number) {
    return array.reduce(
        (acc, curr) => {
            acc[curr > number ? 'greaterThan' : curr < number ? 'smallerThan' : 'equal']++;
            return acc;
        },
        { greaterThan: 0, smallerThan: 0, equal: 0 }
    );
  }

  // Fetching table data from server
  const fetchTableData = useCallback(async (page=1, pageSize=pageSize) => {
    try {
      const data = await getTableContent(app, model, page, pageSize);
      return data;
    } catch (error) {
      console.error(error);
    }
  }, [getTableContent, app, model]);

  useEffect(() => {
    if (!isFirstRender && !pagination.listPages.includes(pagination.currentPageIndex)) {
      return;
    }

    fetchTableData(pagination.currentPageIndex + 1, pageSize).then((data) => {

      const itemsCount = Math.ceil(data['model_instances']['count'] / pageSize);
      const countArray = itemsCount > 0 ? Array.from({ length: itemsCount }, (_, index) => index) : [];

      const paginationStatus = countNumbers(countArray, pagination.currentPageIndex);
      setPagination (prevState => ({
        ...prevState,
        table: data,
        listPages: countArray,
        hasPreviousPage: paginationStatus.smallerThan,
        hasNextPage: paginationStatus.greaterThan,
      }));
      if (isFirstRender) setIsFirstRender(false);
    });

    // For testing and reserve
    // if (process.env.NODE_ENV !== 'production') {}
  }, [pagination.currentPageIndex, pageSize]);

  // Updating rows selection
  useEffect(() => {
    if (checkboxRef.current) {
      checkboxRef.current.indeterminate =
        selectedFlatRows.length > 0 && selectedFlatRows.length !== page.length;
    }

    if (enterClicked) {
      handleSendSelectedRows();
    }

    setSelectedIdParent(selectedId);

    const updateSelectedRowIds = () => {
      data.forEach((row, index) => {
        if (selectedId.includes(row.id) && !selectedRowIds[index]) {
          toggleRowSelected(index, true);
        } else if (!selectedId.includes(row.id) && selectedRowIds[index]) {
          toggleRowSelected(index, false);
        }
      });
    };
  
    updateSelectedRowIds();  

  }, [selectedFlatRows, page, enterClicked, selectedId, data, selectedRowIds, toggleRowSelected]);
  
  // Returning last data
  const handleSendSelectedRows = () => {
    onSelectedIdsChange(selectedId);
  };

  // Rendering table
  return (
    <div>
      <Table striped bordered {...getTableProps()}>
        <thead>
          <tr>
            {headerGroups.map((headerGroup) =>
              headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))
            )}
          </tr>
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, index) => {
            prepareRow(row);
            const isRowSelected = selectedRowIds[row.id];

            return (
              <tr
                {...row.getRowProps()}
                className={row.isSelected ? 'selected' : ''} 
                onClick={() => {
                  if (!editable) return;
                  many ? (
                    row.toggleRowSelected(),
                    handleCheckboxChange(row.original.id)
                  ) : null
                }}
              >
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </Table>
      <div>
        <button onClick={() => 
                  setPagination(prevState => ({
                    ...prevState,
                    currentPageIndex: 0
                  }))
        } disabled={!pagination.hasPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => 
                  setPagination(prevState => ({
                    ...prevState,
                    currentPageIndex: prevState.currentPageIndex - 1
                  }))
        } disabled={!pagination.hasPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => 
                  setPagination(prevState => ({
                    ...prevState,
                    currentPageIndex: prevState.currentPageIndex + 1
                  }))
        } disabled={!pagination.hasNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() =>
                  setPagination(prevState => ({
                    ...prevState,
                    currentPageIndex: prevState.listPages.length - 1
                  }))
        } disabled={!pagination.hasNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pagination.currentPageIndex + 1} of {pagination.listPages.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            defaultValue={pagination.currentPageIndex + 1}
            onChange={(e) => {
              const pageNumber = e.target.value ? Number(e.target.value) - 1 : 0;
              setPagination (prevState => ({
                ...prevState,
                currentPageIndex: pageNumber,
              }));
            }}
            style={{ width: '50px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={(e) => {
            setPageSize(Number(e.target.value));
          }}
        >
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}


const TooltipComponent = ({ targetElementId, tooltipText }) => {
  useEffect(() => {
    const targetElement = document.getElementById(targetElementId);
    const tooltipRoot = document.createElement('div');
    document.body.appendChild(tooltipRoot);

    const tooltip = (
      <Overlay
        show={true}
        target={targetElement}
        placement="top"
        transition={false}
      >
        {({ placement, arrowProps, show: _show, popper, ...props }) => (
          <div
            {...props}
            style={{
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              padding: '10px',
              color: 'white',
              borderRadius: '3px',
              ...props.style,
            }}
          >
            {tooltipText}
          </div>
        )}
      </Overlay>
    );

    ReactDOM.render(tooltip, tooltipRoot);

    return () => {
      ReactDOM.unmountComponentAtNode(tooltipRoot);
      document.body.removeChild(tooltipRoot);
    };
  }, [targetElementId, tooltipText]);

  return null;
};


export { TModal, DynamicTableComponent };
