import { useEffect, useMemo, useState } from 'react';
import { propertyService } from '../services/propertyService';
import SearchBar from '../components/SearchBar';
import FilterPanel from '../components/FilterPanel';
import LoadingSkeleton from '../components/LoadingSkeleton';
import PropertyGrid from '../components/PropertyGrid';
import Pagination from '../components/Pagination';
import EmptyState from '../components/EmptyState';

const defaultFilters = {
  bhk: '',
  priceRange: '',
  city: '',
  state: '',
  bedrooms: '',
  bathrooms: ''
};

export default function PropertySearchPage() {
  const [filters, setFilters] = useState(defaultFilters);
  const [search, setSearch] = useState('');
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ page: 1, totalPages: 1 });

  const parsedRange = useMemo(() => {
    if (!filters.priceRange) return {};
    const [minPrice, maxPrice] = filters.priceRange.split('-').map((value) => Number(value.trim()));
    return {
      minPrice: Number.isFinite(minPrice) ? minPrice : undefined,
      maxPrice: Number.isFinite(maxPrice) ? maxPrice : undefined
    };
  }, [filters.priceRange]);

  useEffect(() => {
    const fetchProperties = async () => {
      setLoading(true);
      const response = await propertyService.getProperties({
        ...parsedRange,
        bhk: filters.bhk,
        city: filters.city,
        state: filters.state,
        bedrooms: filters.bedrooms,
        bathrooms: filters.bathrooms,
        query: search,
        page,
        pageSize: 6
      });

      setProperties(response.data || []);
      setPagination(response.pagination || { page: 1, totalPages: 1 });
      setLoading(false);
    };

    fetchProperties();
  }, [filters, parsedRange, page, search]);

  const handleFilterChange = (nextFilters) => {
    setFilters(nextFilters);
    setPage(1);
  };

  const handleSearch = (event) => {
    event.preventDefault();
    setPage(1);
  };

  return (
    <div className="space-y-6">
      <SearchBar
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        onSubmit={handleSearch}
        placeholder="Search by city, locality, or property name"
      />

      <FilterPanel filters={filters} onChange={handleFilterChange} />

      {loading ? (
        <LoadingSkeleton count={6} />
      ) : properties.length ? (
        <>
          <PropertyGrid properties={properties} />
          <Pagination page={pagination.page} totalPages={pagination.totalPages} onPageChange={setPage} />
        </>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}