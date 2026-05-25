import os
import psycopg2
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_chroma import Chroma

from .embedding import get_embeddings

load_dotenv()


def ingest_products():

    # -----------------------------
    # PostgreSQL Connection
    # -----------------------------
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    # -----------------------------
    # Fetch Products
    # -----------------------------
    query = """
    SELECT
        p.id,
        p.title,
        p.description,
        p.brand_name,
        p.material,
        p.color,
        p.locality,
        p.price_per_day,
        c.category
    FROM products_product p
    LEFT JOIN products_category c
    ON p.category_id = c.id
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print(f"✅ Found {len(rows)} products")

    documents = []

    # -----------------------------
    # Convert Products -> Documents
    # -----------------------------
    for row in rows:

        product_id = row[0]
        title = row[1]
        description = row[2]
        brand = row[3]
        material = row[4]
        color = row[5]
        locality = row[6]
        price = row[7]
        category = row[8]

        text = f"""
        Product: {title}
        Category: {category}
        Brand: {brand}
        Description: {description}
        Material: {material}
        Color: {color}
        Location: {locality}
        Price per day: ₹{price}
        """

        doc = Document(
            page_content=text,
            metadata={
                "product_id": product_id,
                "title": title,
                "price_per_day": str(price),
                "locality": locality or "",
                "category": category or ""
            }
        )

        documents.append(doc)

    # -----------------------------
    # Embeddings
    # -----------------------------
    embeddings = get_embeddings()

    # -----------------------------
    # Create / Load Chroma DB
    # -----------------------------
    vectorstore = Chroma(
        collection_name="products",
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )

    # -----------------------------
    # Delete Old Collection
    # -----------------------------
    try:
        vectorstore.delete_collection()
        print("🗑️ Old collection deleted")
    except Exception as e:
        print("⚠️ No old collection found")
        print(e)

    # -----------------------------
    # Recreate Collection
    # -----------------------------
    vectorstore = Chroma(
        collection_name="products",
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )

    # -----------------------------
    # Add Documents
    # -----------------------------
    vectorstore.add_documents(documents)

    print(f"✅ Ingested {len(documents)} products")

    # -----------------------------
    # Close DB Connection
    # -----------------------------
    cursor.close()
    conn.close()


if __name__ == "__main__":
    ingest_products()








# import os
# import psycopg2
# import shutil

# from dotenv import load_dotenv

# from langchain_core.documents import Document
# from langchain_chroma import Chroma

# from .embedding import get_embeddings

# load_dotenv()


# def ingest_products():

#     conn = psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         port=os.getenv("DB_PORT")
#     )

#     cursor = conn.cursor()

#     query = """
#     SELECT
#         p.id,
#         p.title,
#         p.description,
#         p.brand_name,
#         p.material,
#         p.color,
#         p.locality,
#         p.price_per_day,
#         c.category
#     FROM products_product p
#     LEFT JOIN products_category c
#     ON p.category_id = c.id
#     """

#     cursor.execute(query)

#     rows = cursor.fetchall()

#     print(f"✅ Found {len(rows)} products")

#     documents = []

#     for row in rows:

#         product_id = row[0]
#         title = row[1]
#         description = row[2]
#         brand = row[3]
#         material = row[4]
#         color = row[5]
#         locality = row[6]
#         price = row[7]
#         category = row[8]

#         text = f"""
#         Product: {title}
#         Category: {category}
#         Brand: {brand}
#         Description: {description}
#         Material: {material}
#         Color: {color}
#         Location: {locality}
#         Price per day: ₹{price}
#         """

#         doc = Document(
#             page_content=text,
#             metadata={
#                 "product_id": product_id,
#                 "title": title,
#                 "price_per_day": str(price),
#                 "locality": locality or ""
#             }
#         )

#         documents.append(doc)


#     if os.path.exists("./chroma_db"):
#         shutil.rmtree("./chroma_db")

#     embeddings = get_embeddings()

#     vectorstore = Chroma(
#         persist_directory="./chroma_db",
#         embedding_function=embeddings
#     )

#     vectorstore.add_documents(documents)

#     print(f"✅ Ingested {len(documents)} products")

#     cursor.close()
#     conn.close()


# if __name__ == "__main__":
#     ingest_products()


