"""
management of "history" of stored blobs, grouped
by some 'session id'. Overwrites are not supported by design.
"""

from cassandra.query import SimpleStatement

import cassio.cql


class StoredBlobHistory:

    def __init__(self, session, keyspace, table_name):
        self.session = session
        self.keyspace = keyspace
        self.table_name = table_name
        # Schema creation, if needed
        cql = SimpleStatement(cassio.cql.create_session_table.format(
            keyspace=self.keyspace,
            table_name=self.table_name,
        ))
        session.execute(cql)

    def store(self, session_id, blob, ttl_seconds):
        if ttl_seconds:
            ttl_spec = f' USING TTL {ttl_seconds}'
        else:
            ttl_spec = ''
        #
        cql = SimpleStatement(cassio.cql.store_session_blob.format(
            keyspace=self.keyspace,
            table_name=self.table_name,
            ttlSpec=ttl_spec,
        ))
        self.session.execute(
            cql,
            (
                session_id,
                blob,
            )
        )

    def retrieve(self, session_id, max_count=None):
        pass
        cql = SimpleStatement(cassio.cql.get_session_blobs.format(
            keyspace=self.keyspace,
            table_name=self.table_name,
        ))
        rows = self.session.execute(
            cql,
            (session_id,)
        )
        return (
            row.blob
            for row in rows
        )

    def clear_session_id(self, session_id):
        pass
        cql = SimpleStatement(cassio.cql.clear_session.format(
            keyspace=self.keyspace,
            table_name=self.table_name,
        ))
        self.session.execute(cql, (session_id,))
