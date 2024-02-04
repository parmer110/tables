import React, { useState, useRef, useEffect, useMemo } from 'react';
import ReactDOM from "react-dom";
import { useTable, usePagination, useFilters, useRowSelect } from 'react-table';
import { Table, Modal, Button, Form, Alert, Card } from 'react-bootstrap';
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
            <Button variant="primary" disabled={editable} onClick={() => {
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


function DynamicTableComponent({ table, many, values, editable, enterClicked, onSelectedIdsChange, setSelectedIdParent }) {
  
  let ids = Array.isArray(values) ? values : [values];
  const checkboxRef = useRef();
  const [selectedId, setSelectedId] = useState(ids);

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

  let columns = useMemo(
    () =>
      [
        {
          Header: 'id',
          accessor: 'id0'
        },
        ...table.field_info
          .filter(field => !['created_at', 'updated_at', 'deleted_at'].includes(field.name))
          .map((field, index) => ({
            Header: field.name,
            accessor: field.name,
          }))
      ],
    [table.field_info, selectedId]
  );

  const data = useMemo(
    () =>
      table.model_instances.results.map((record, index) => {
        const row = {};
        table.field_info.forEach((field) => {
          if (field.name !== 'created_at' && field.name !== 'updated_at' && field.name !== 'deleted_at') {
            row[field.name] = record[field.name];
          }
        });
        row.id0 = index + 1;
        return row;
      }),
    [table.field_info, table.model_instances.results]
  );

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
                disabled={editable}
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
                disabled={editable}
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
                disabled={editable}
              />
            )
          ),
        },
        ...columns,
      ]);
    }    
  );

  useEffect(() => {
    if (checkboxRef.current) {
      checkboxRef.current.indeterminate =
        selectedFlatRows.length > 0 && selectedFlatRows.length !== page.length;
    }

    if (enterClicked) {
      handleSendSelectedRows();
    }

    setSelectedIdParent(selectedId);

  }, [selectedFlatRows, page, enterClicked, selectedId]);
  
  const handleSendSelectedRows = () => {
    onSelectedIdsChange(selectedId);
  };

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
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={(e) => {
              const pageNumber = e.target.value ? Number(e.target.value) - 1 : 0;
              gotoPage(pageNumber);
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

export { TModal, DynamicTableComponent };
