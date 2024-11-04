from PIL import Image
import os

def convert_and_resize_image(input_path, output_path):
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert image to RGB mode if it's not already
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image to 256x256 maintaining aspect ratio
            img.thumbnail((256, 256))
            
            # Create a new white background image
            new_img = Image.new('RGB', (256, 256), (255, 255, 255))
            
            # Calculate position to paste the resized image
            x = (256 - img.size[0]) // 2
            y = (256 - img.size[1]) // 2
            
            # Paste the resized image onto the white background
            new_img.paste(img, (x, y))
            
            # Save as PNG
            new_img.save(output_path, 'PNG')
            print(f"Successfully converted and resized: {output_path}")
            
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def process_directory(input_dir, output_dir):
    # Create input and output directories if they don't exist
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created input directory: {input_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Supported image formats
    supported_formats = ['.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in supported_formats:
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_dir, output_filename)
            convert_and_resize_image(input_path, output_path)

if __name__ == "__main__":
    # Example usage
    input_directory = "input_images"
    output_directory = "output_images"
    
    process_directory(input_directory, output_directory)