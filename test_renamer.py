import os
import shutil
import tempfile
import unittest

from sanitizer import caption_to_filename, clean_caption
from renamer_core import scan_images, get_unique_filename

class TestSanitizer(unittest.TestCase):
    def test_clean_caption_strips_fillers(self):
        caption = "A photo of a cute orange cat sitting on a couch."
        cleaned = clean_caption(caption)
        self.assertNotIn("a photo of", cleaned)
        self.assertIn("orange cat", cleaned)

    def test_caption_to_filename_word_limit(self):
        # 1 to 5 words max
        caption = "A high resolution photo of an ultra fast red sports car driving down a mountain road"
        result = caption_to_filename(caption, min_words=1, max_words=5, separator="_")
        words = result.split("_")
        self.assertGreaterEqual(len(words), 1)
        self.assertLessEqual(len(words), 5)
        self.assertEqual(result, result.lower())

    def test_caption_to_filename_short_caption(self):
        caption = "Golden retriever"
        result = caption_to_filename(caption, min_words=1, max_words=5, separator="_")
        self.assertEqual(result, "golden_retriever")

    def test_caption_to_filename_special_chars(self):
        caption = "Sunrise: over the mountains! (4k, ultra-hdr?)"
        result = caption_to_filename(caption, min_words=1, max_words=5, separator="_")
        self.assertNotIn(":", result)
        self.assertNotIn("!", result)
        self.assertNotIn("(", result)
        self.assertNotIn("?", result)
        self.assertTrue(all(c.isalnum() or c in "_-" for c in result))

    def test_windows_reserved_names(self):
        caption = "con"
        result = caption_to_filename(caption, min_words=1, max_words=5)
        self.assertNotEqual(result, "con")
        self.assertEqual(result, "con_img")

class TestRenamerCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "subfolder")
        os.makedirs(self.sub_dir, exist_ok=True)

        # Create dummy image files
        self.img1 = os.path.join(self.test_dir, "photo1.jpg")
        self.img2 = os.path.join(self.test_dir, "graphic.png")
        self.img_sub = os.path.join(self.sub_dir, "nested_photo.jpeg")

        # Create dummy non-image files (must NOT be touched)
        self.txt1 = os.path.join(self.test_dir, "notes.txt")
        self.doc1 = os.path.join(self.test_dir, "document.docx")
        self.mp4 = os.path.join(self.sub_dir, "video.mp4")

        for f in [self.img1, self.img2, self.img_sub, self.txt1, self.doc1, self.mp4]:
            with open(f, "w", encoding="utf-8") as fp:
                fp.write("test content")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scan_images_recursive(self):
        images = scan_images(self.test_dir, recursive=True)
        # Should only find 3 images, 0 non-images
        self.assertEqual(len(images), 3)
        self.assertTrue(any("photo1.jpg" in img for img in images))
        self.assertTrue(any("graphic.png" in img for img in images))
        self.assertTrue(any("nested_photo.jpeg" in img for img in images))

        # Ensure non-images are strictly excluded
        for img in images:
            self.assertFalse(img.endswith(".txt"))
            self.assertFalse(img.endswith(".docx"))
            self.assertFalse(img.endswith(".mp4"))

    def test_scan_images_non_recursive(self):
        images = scan_images(self.test_dir, recursive=False)
        # Only direct images: photo1.jpg and graphic.png
        self.assertEqual(len(images), 2)
        for img in images:
            self.assertFalse("nested_photo" in img)

    def test_get_unique_filename_no_collision(self):
        new_name, new_path = get_unique_filename(self.test_dir, "sleeping_cat", ".jpg", self.img1)
        self.assertEqual(new_name, "sleeping_cat.jpg")
        self.assertEqual(new_path, os.path.join(self.test_dir, "sleeping_cat.jpg"))

    def test_get_unique_filename_with_collision(self):
        # Create an existing file named sleeping_cat.jpg
        existing = os.path.join(self.test_dir, "sleeping_cat.jpg")
        with open(existing, "w") as f:
            f.write("existing")

        new_name, new_path = get_unique_filename(self.test_dir, "sleeping_cat", ".jpg", self.img1)
        self.assertEqual(new_name, "sleeping_cat_1.jpg")
        self.assertEqual(new_path, os.path.join(self.test_dir, "sleeping_cat_1.jpg"))

if __name__ == "__main__":
    unittest.main()
