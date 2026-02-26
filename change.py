import fitz  # PyMuPDF
import os

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):

    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file tại {pdf_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        doc = fitz.open(pdf_path)
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        
        print(f"Đang xử lý file: {filename}")
        print(f"Tổng số trang: {len(doc)}")
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            output_file = os.path.join(output_folder, f"{filename}_page_{page_num + 1:03d}.png")
            pix.save(output_file)
            print(f" -> Đã lưu: {output_file} (Độ phân giải: {pix.width}x{pix.height})")

        print("\nHoàn tất chuyển đổi!")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

my_pdf_path = "anh.pdf" 
my_output_folder = "Result"

if __name__ == "__main__":
    convert_pdf_to_images(my_pdf_path, my_output_folder, dpi=300)