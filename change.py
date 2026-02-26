import fitz  # PyMuPDF
import os

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """
    Chuyển đổi PDF sang ảnh với chất lượng cao.
    
    :param pdf_path: Đường dẫn tới file PDF
    :param output_folder: Thư mục lưu ảnh đầu ra
    :param dpi: Độ phân giải (300 là chuẩn in ấn rất nét, 
                nếu muốn nhẹ hơn có thể để 150 hoặc 200)
    """
    
    # Kiểm tra file tồn tại
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file tại {pdf_path}")
        return

    # Tạo thư mục đầu ra nếu chưa có
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Mở file PDF (PyMuPDF xử lý file lớn rất tốt vì nó không load hết vào RAM)
        doc = fitz.open(pdf_path)
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        
        print(f"Đang xử lý file: {filename}")
        print(f"Tổng số trang: {len(doc)}")
        
        # Tính toán mức độ phóng to (Zoom) dựa trên DPI mong muốn
        # Mặc định PDF là 72 DPI. Để lên 300 DPI thì zoom = 300 / 72
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # get_pixmap chuyển vector thành ảnh bitmap
            # alpha=False: Ép nền trắng (tránh lỗi hiển thị màu trên nền trong suốt)
            # colorspace="csRGB": Đảm bảo màu sắc chuẩn mắt nhìn
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            output_file = os.path.join(output_folder, f"{filename}_page_{page_num + 1:03d}.png")
            
            # Lưu file
            pix.save(output_file)
            print(f" -> Đã lưu: {output_file} (Độ phân giải: {pix.width}x{pix.height})")

        print("\nHoàn tất chuyển đổi!")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

# --- CẤU HÌNH ---
# Thay đổi đường dẫn file của bạn ở đây
my_pdf_path = "anh.pdf" 
my_output_folder = "Result"

# Chạy chương trình
if __name__ == "__main__":
    # DPI 300 là rất nét. Nếu file quá to ảnh hưởng tốc độ, hãy thử giảm xuống 200.
    convert_pdf_to_images(my_pdf_path, my_output_folder, dpi=300)