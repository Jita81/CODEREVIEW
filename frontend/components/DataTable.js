// DataTable.js - Complex component with performance and security issues

import React, { useState, useEffect, useMemo } from 'react';
import { getUsersList } from '../services/userService';

const DataTable = ({ initialData = [], columns = [], onRowClick }) => {
    const [data, setData] = useState(initialData);
    const [sortConfig, setSortConfig] = useState(null);
    const [filterText, setFilterText] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [loading, setLoading] = useState(false);
    const [selectedRows, setSelectedRows] = useState(new Set());

    // GLARING ISSUE: useEffect with missing dependencies causing infinite re-renders
    useEffect(() => {
        loadData();
    }, [currentPage]); // Missing filterText dependency

    // PERFORMANCE ISSUE: Expensive operation on every render
    const loadData = async () => {
        setLoading(true);
        try {
            // PERFORMANCE ISSUE: Loading all data instead of paginated data
            const allUsers = await getUsersList(1, 10000); // Too much data
            setData(allUsers);
        } catch (error) {
            // SUBTLE ISSUE: Not handling errors properly
            console.error('Failed to load data:', error);
        } finally {
            setLoading(false);
        }
    };

    // PERFORMANCE ISSUE: Not memoizing expensive computations
    const filteredData = data.filter(row => {
        // GLARING ISSUE: XSS vulnerability in filtering
        const searchText = filterText.toLowerCase();
        return Object.values(row).some(value => {
            if (typeof value === 'string') {
                // SECURITY ISSUE: No input sanitization
                return value.toLowerCase().includes(searchText);
            }
            return false;
        });
    });

    // PERFORMANCE ISSUE: Sorting recalculated on every render
    const sortedData = useMemo(() => {
        if (!sortConfig) return filteredData;
        
        // PERFORMANCE ISSUE: Inefficient sorting algorithm for large datasets
        return [...filteredData].sort((a, b) => {
            const aValue = a[sortConfig.key];
            const bValue = b[sortConfig.key];
            
            // SUBTLE ISSUE: Not handling null/undefined values properly
            if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
            return 0;
        });
    }, [filteredData, sortConfig]); // PERFORMANCE ISSUE: filteredData changes on every render

    // SUBTLE ISSUE: Pagination logic doesn't handle edge cases
    const pageSize = 10;
    const totalPages = Math.ceil(sortedData.length / pageSize);
    const paginatedData = sortedData.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    );

    const handleSort = (key) => {
        setSortConfig(prevConfig => ({
            key,
            direction: prevConfig?.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc'
        }));
    };

    // PERFORMANCE ISSUE: Creating new functions on every render
    const handleRowSelect = (rowId) => {
        setSelectedRows(prev => {
            const newSet = new Set(prev);
            if (newSet.has(rowId)) {
                newSet.delete(rowId);
            } else {
                newSet.add(rowId);
            }
            return newSet;
        });
    };

    const handleSelectAll = () => {
        if (selectedRows.size === paginatedData.length) {
            setSelectedRows(new Set());
        } else {
            setSelectedRows(new Set(paginatedData.map(row => row.id)));
        }
    };

    // GLARING ISSUE: Dangerous HTML rendering without sanitization
    const renderCell = (row, column) => {
        const value = row[column.key];
        
        if (column.render) {
            return column.render(value, row);
        }
        
        // SECURITY ISSUE: Potential XSS vulnerability
        if (column.allowHtml) {
            return <div dangerouslySetInnerHTML={{ __html: value }} />;
        }
        
        return value;
    };

    // PERFORMANCE ISSUE: Inline styles causing re-renders
    const tableStyle = {
        width: '100%',
        borderCollapse: 'collapse',
        marginTop: '20px'
    };

    const headerStyle = {
        backgroundColor: '#f5f5f5',
        padding: '12px',
        borderBottom: '2px solid #ddd',
        cursor: 'pointer',
        userSelect: 'none'
    };

    if (loading) {
        // PERFORMANCE ISSUE: Complex loading component re-rendered frequently
        return (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '50px' }}>
                <div style={{ 
                    border: '4px solid #f3f3f3',
                    borderTop: '4px solid #3498db',
                    borderRadius: '50%',
                    width: '50px',
                    height: '50px',
                    animation: 'spin 2s linear infinite'
                }}>
                </div>
            </div>
        );
    }

    return (
        <div className="data-table-container">
            <div className="table-controls">
                <input
                    type="text"
                    placeholder="Filter data..."
                    value={filterText}
                    onChange={(e) => setFilterText(e.target.value)}
                    style={{ marginBottom: '20px', padding: '8px', width: '300px' }}
                />
                
                {/* SUBTLE ISSUE: Bulk actions without proper confirmation */}
                <div className="bulk-actions">
                    <button 
                        onClick={handleSelectAll}
                        disabled={paginatedData.length === 0}
                    >
                        {selectedRows.size === paginatedData.length ? 'Deselect All' : 'Select All'}
                    </button>
                    
                    {selectedRows.size > 0 && (
                        <button 
                            onClick={() => {
                                // GLARING ISSUE: Bulk delete without confirmation
                                console.log('Deleting rows:', Array.from(selectedRows));
                                // No actual delete implementation - would be dangerous
                            }}
                            style={{ marginLeft: '10px', backgroundColor: 'red', color: 'white' }}
                        >
                            Delete Selected ({selectedRows.size})
                        </button>
                    )}
                </div>
            </div>

            <table style={tableStyle}>
                <thead>
                    <tr>
                        <th style={headerStyle}>
                            <input 
                                type="checkbox" 
                                checked={selectedRows.size === paginatedData.length && paginatedData.length > 0}
                                onChange={handleSelectAll}
                            />
                        </th>
                        {columns.map(column => (
                            <th 
                                key={column.key}
                                style={{
                                    ...headerStyle,
                                    // PERFORMANCE ISSUE: Complex style calculations on every render
                                    backgroundColor: sortConfig?.key === column.key ? '#e3f2fd' : '#f5f5f5'
                                }}
                                onClick={() => column.sortable !== false && handleSort(column.key)}
                            >
                                {column.label}
                                {sortConfig?.key === column.key && (
                                    <span style={{ marginLeft: '5px' }}>
                                        {sortConfig.direction === 'asc' ? '↑' : '↓'}
                                    </span>
                                )}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {paginatedData.map((row, index) => (
                        <tr 
                            key={row.id || index} // SUBTLE ISSUE: Fallback to index as key
                            style={{
                                // PERFORMANCE ISSUE: Dynamic styles
                                backgroundColor: selectedRows.has(row.id) ? '#e3f2fd' : 
                                                index % 2 === 0 ? '#f9f9f9' : 'white',
                                cursor: onRowClick ? 'pointer' : 'default'
                            }}
                            onClick={() => onRowClick && onRowClick(row)}
                        >
                            <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>
                                <input 
                                    type="checkbox"
                                    checked={selectedRows.has(row.id)}
                                    onChange={() => handleRowSelect(row.id)}
                                    onClick={(e) => e.stopPropagation()} // Prevent row click
                                />
                            </td>
                            {columns.map(column => (
                                <td 
                                    key={`${row.id}-${column.key}`}
                                    style={{ padding: '8px', borderBottom: '1px solid #ddd' }}
                                >
                                    {renderCell(row, column)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* SUBTLE ISSUE: Pagination doesn't handle edge cases properly */}
            <div className="pagination" style={{ marginTop: '20px', textAlign: 'center' }}>
                <button 
                    onClick={() => setCurrentPage(1)}
                    disabled={currentPage === 1}
                >
                    First
                </button>
                <button 
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    style={{ marginLeft: '5px' }}
                >
                    Previous
                </button>
                
                <span style={{ margin: '0 20px' }}>
                    Page {currentPage} of {totalPages} ({sortedData.length} total records)
                </span>
                
                <button 
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    style={{ marginRight: '5px' }}
                >
                    Next
                </button>
                <button 
                    onClick={() => setCurrentPage(totalPages)}
                    disabled={currentPage === totalPages}
                >
                    Last
                </button>
            </div>

            {/* GLARING ISSUE: Debug information exposed in production */}
            {process.env.NODE_ENV === 'development' && (
                <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
                    <h4>Debug Info:</h4>
                    <p>Total Data: {data.length} items</p>
                    <p>Filtered Data: {filteredData.length} items</p>
                    <p>Selected Rows: {selectedRows.size} items</p>
                    <p>Sort Config: {JSON.stringify(sortConfig)}</p>
                    {/* SECURITY ISSUE: Potentially exposing sensitive data */}
                    <p>Sample Data: {JSON.stringify(data.slice(0, 2))}</p>
                </div>
            )}
        </div>
    );
};

export default DataTable;
