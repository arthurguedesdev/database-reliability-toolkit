CREATE TABLE public.customers (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    region text NOT NULL
);
CREATE TABLE public.orders (
    id bigint PRIMARY KEY,
    customer_id bigint NOT NULL REFERENCES public.customers(id),
    created_at timestamptz NOT NULL,
    amount numeric(12,2) NOT NULL CHECK (amount >= 0),
    status text NOT NULL CHECK (status IN ('paid', 'pending', 'cancelled'))
);
INSERT INTO public.customers(id, name, region)
SELECT i, 'Customer ' || i, (ARRAY['SP','RJ','MG','PR','BA'])[1 + (i % 5)]
FROM generate_series(1, 10000) AS i;
INSERT INTO public.orders(id, customer_id, created_at, amount, status)
SELECT i, 1 + (i % 10000), now() - (i % 365) * interval '1 day',
       ((i % 10000) + 100)::numeric / 10,
       (ARRAY['paid','paid','paid','pending','cancelled'])[1 + (i % 5)]
FROM generate_series(1, 100000) AS i;
CREATE INDEX idx_orders_customer_id ON public.orders(customer_id);
CREATE INDEX idx_orders_created_at ON public.orders(created_at);
ANALYZE public.customers;
ANALYZE public.orders;
